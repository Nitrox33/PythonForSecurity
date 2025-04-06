from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import argparse
import os

class Signer:
    def __init__(self, generate=False, key_size: int = 4096):
        if generate:
            self.private_key, self.public_key = self.generate_rsa_keypair(key_size=key_size)
        else:
            self.private_key, self.public_key = None, None
            
        self.hasher = SHA256.new()
        self.signer = pkcs1_15.new(self.private_key)

    def reset(self):
        self.hasher = SHA256.new()
        self.signer = pkcs1_15.new(self.private_key)

    def generate_rsa_keypair(self,key_size: int = 4096) -> tuple:
        """Generate an RSA key pair.

        Args:
            key_size (int): Size of the RSA key in bits. Default is 4096.

        Returns:
            tuple: A tuple containing the private and public keys.
        """
        private_key = RSA.generate(key_size)
        public_key = private_key.publickey()
        return private_key, public_key

    def sign_message(self, message: bytes) -> bytes:
        """Sign a message using the private key.

        Args:
            message (bytes): The message to sign.

        Returns:
            bytes: The signature.
        """
        self.hasher.update(message)
        signature = self.signer.sign(self.hasher)
        self.reset()  # Reset the hasher and signer for future use
        return signature

    def import_key(self, private_key_path:str=None, public_key_path:str=None) -> None:
        """Import RSA keys from files.

        Args:
            private_key_path (str): Path to the private key file.
            public_key_path (str): Path to the public key file.
        """
        if private_key_path:
            with open(private_key_path, "rb") as f:
                private_key = f.read()
            self.private_key = RSA.import_key(private_key)
            self.signer = pkcs1_15.new(self.private_key)  # Reinitialize signer with the new private key
        if public_key_path:
            with open(public_key_path, "rb") as f:
                public_key = f.read()
            self.public_key = RSA.import_key(public_key)
            if self.private_key is None:
                self.signer = pkcs1_15.new(self.public_key)  # Reinitialize signer with the new public key

    def export_key(self, private_key_name:str="private_key.pem", public_key_name:str="public_key.pem") -> bytes:
        """Export the public key.

        Returns:
            bytes: The public key in PEM format.
        """
        private_key_pem = self.private_key.export_key(format='PEM')
        public_key_pem = self.public_key.export_key(format='PEM')
        
        with open(private_key_name, "wb") as f:
            f.write(private_key_pem)
        with open(public_key_name, "wb") as f:
            f.write(public_key_pem)
        return

    def verify(self, message: bytes, signature: bytes) -> bool:
        """Verify the signature of a message using the public key.

        Args:
            message (bytes): The original message.
            signature (bytes): The signature to verify.

        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        self.hasher.update(message)
        try:
            pkcs1_15.new(self.public_key).verify(self.hasher, signature)
            return True
        except (ValueError, TypeError):
            return False

def main():
    parser = argparse.ArgumentParser(description="RSA Sign and Verify")
    parser.add_argument("-g", "--generate",action="store_true" , help="Generate RSA key pair")
    parser.add_argument("-i", "--input", type=str, help="Input file to sign")
    parser.add_argument("-s", "--signature", type=str, help="Input file to verify")
    parser.add_argument("--sign", action="store_true", help="Sign the input file")
    parser.add_argument("--verify",action="store_true" , help="Verify the following signature")
    parser.add_argument("-pub_k", "--public_key", type=str, help="Key file for verifying")
    parser.add_argument("-priv_k", "--private_key", type=str, help="Key file for signing")
    parser.add_argument("-o", "--output", type=str, help="Output file for the signature")
    
    args = parser.parse_args()
    
    if args.generate:
        # Generate RSA key pair if requested
        signer = Signer(generate=True)
        signer.export_key()
        print("RSA key pair generated and saved as 'private_key.pem' and 'public_key.pem'.")
        return
    
    # verify the arguments
    if not args.input:
        print("You must provide an input file to sign or verify.")
        return
    if not args.sign and not args.verify:
        print("You must specify either --sign or --verify.")
        return
    if not args.public_key and args.verify:
        print("You must provide a public key file for verification.")
        return
    if not args.private_key and args.sign:
        print("You must provide a private key file for signing.")
        return
    if args.sign and not os.path.exists(args.private_key):
        print("The private key file does not exist.")
        return
    if args.verify and not os.path.exists(args.public_key):
        print("The public key file does not exist.")
        return
    
    # check if the input file exists
    if not os.path.exists(args.input):
        message = args.input.encode()
    else:
        with open(args.input, "rb") as f:
            message = f.read()
    
    # import the signature
    if args.signature:
        if not os.path.exists(args.signature):
            signature = args.signature.encode()
        else:
            with open(args.signature, "rb") as f:
                signature = f.read()
    
    
    SIGNER = Signer()
    SIGNER.import_key(private_key_path=args.private_key, public_key_path=args.public_key)
    if args.sign:
        signature = SIGNER.sign_message(message)
        if args.output:
            with open(args.output, "wb") as f:
                f.write(signature)
        print(f"Signature: {signature.hex()}")
    elif args.verify:
        is_valid = SIGNER.verify(message, signature)
        if is_valid:
            print("Signature is valid.")
        else:
            print("Signature is invalid.")
    else:
        print("You must specify either --sign or --verify.")

if __name__ == "__main__":
    main()