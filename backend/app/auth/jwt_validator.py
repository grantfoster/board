import jwt
import httpx
import base64
from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from .config import azure_ad_config


class JWTValidator:
    """
    validates Entra JWT tokens.

    handles fetching Entra public keys anfd validating JWT tokens against them/checking for expiry.
    """

    def __init__(self):
        self.config = azure_ad_config
        self.jwks_cache = None
        self.jwks_cache_time = None

    async def validate_token(self, token: str) -> Dict[str, Any]:
        """
        validates JWT token from Entra/Azure AD.

        Args:
            token: JWT token to validate

        Returns:
            the decoded token if valid

        Raises:
            HTTPException: if our token is invalid or malformed.
        """
        try:
            # decode the header to get the key ID (kid)
            header = jwt.get_unverified_header(token)
            kid = header.get("kid")

            if not kid:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: missing key ID",
                )

            public_key = await self._get_public_key(kid)

            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience=self.config.audience,
                issuer=self.config.issuer,
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_aud": True,
                    "verify+iss": True,
                },
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )
        except jwt.InvalidAudienceError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid audience"
            )
        except jwt.InvalidIssuerError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid issuer"
            )
        except jwt.InvalidSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

    async def _get_public_key(self, kid: str) -> str:
        """
        Gets the public key from the Entra JWKS endpoint.

        Args:
            kid: the key id from the header

        Returns:
            the public key as a string

        Raises:
            HTTPException: if unable to fetch or find the key
        """
        jwks = await self._fetch_jwks()

        # find the key with matching kid
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                return self._jwk_to_pem(key)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to find public key for token",
        )

    async def _fetch_jwks(self) -> Dict[str, Any]:
        """
        fetches the json web key set from Entra.

        Returns:
            jwks as a dictionary.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(self.config.jwks_url)
            response.raise_for_status()
            return response.json()

    def _jwk_to_pem(self, jwk: Dict[str, Any]) -> str:
        """
        converts a jwk to pem.

        Args:
            jwk: a dictionary of jwks from entra public keys

        Returns:
            public key in pem format
        """
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization

        # extract rsa key components from the jwk
        # these are two large numbers: n which is a modulus and e - exponent
        # these come in base64url format ane here we decode it
        n = int.from_bytes(base64.urlsafe_b64decode(jwk["n"] + "=="), "big")
        e = int.from_bytes(base64.urlsafe_b64decode(jwk["e"] + "=="), "big")

        # reconstruct the RSA public key from the components
        # RSAPublicNumbers takes the modulus (n) and exponent (e) and creates
        # a cryptography object that represents the public key
        public_key = rsa.RSAPublicNumbers(e, n).public_key()

        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        return pem.decode("utf-8")


jwt_validator = JWTValidator()
