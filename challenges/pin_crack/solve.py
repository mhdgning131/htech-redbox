import hashlib

# Paramètres du challenge
target_salt_hex = "71475423dcd33669"
target_hash = "aac4a8294bf0c218f53b33e7e673153187ea1f320adc6ab48ab6aac2a1d25e06"

# Conversion du salt en bytes
salt_bytes = bytes.fromhex(target_salt_hex)

print("[*] Démarrage du bruteforce PIN 4 chiffres...")

# Boucle de 0000 à 9999
for i in range(10000):
    pin = f"{i:04d}"  # Format 4 chiffres (ex: 0042)
    
    # Construction de la donnée à hasher : Salt + PIN
    # Note: Le PIN est traité comme une chaîne de caractères encodée en utf-8/ascii
    data = salt_bytes + pin.encode()
    
    # Calcul du hash
    computed_hash = hashlib.sha256(data).hexdigest()
    
    if computed_hash == target_hash:
        print(f"[+] PIN TROUVÉ : {pin}")
        break
else:
    print("[-] PIN non trouvé.")
