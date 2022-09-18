# DAn: Duke Animation

import png, argparse, struct

HDR = "<HHIB"
ENTRY = "<I"

def select(files):
    mx = 0
    my = 0
    isalpha = 0

    for i in files:
        with open(i, "rb") as f:
            width = int.from_bytes(f.read(2), "little")
            height = int.from_bytes(f.read(2), "little")
            print(width, height)
            f.read(4)
            alpha = int.from_bytes(f.read(1), "little")

            if width > mx and height > my:
                mx, my = width, height

            if isalpha == 1 and alpha == 0:
                print("Error: Cannot mix alpha and non-alpha images!!!")
                exit(1)
            else:
                isalpha = alpha
    print(f"Selected maximal size: {mx}x{my}")
    return mx, my, isalpha

def make_body(files) -> bytes:
    bag = b''
    for i in files:
        with open(i, "rb") as f:
            datas = list(f.read(4))
            if datas==[0x89, 0x50, 0x4E, 0x47]:
                print("Error: Cannot use PNG files here. Use Duke Images instead.")
            bag += struct.pack(ENTRY, int.from_bytes(f.read(4), "little"))
            bag += f.read()
            f.close()
    return bag

def main(args):
    files = args.file
    filecount = len(files)

    out = files[0].split(".")[0]+".dan"

    width, height, alpha = select(files)

    print(f"Parameters:\n\tWidth: {width}\n\tHeight: {height}\n\tAlpha: {bool(alpha)}")

    with open(out, "wb") as file:
        file.write(
            b"DAN_"+
            struct.pack(
                HDR,
                width, height,
                filecount, alpha
            )
        )

        file.write(make_body(files))
        file.truncate()
        file.flush()

        file.close()

if __name__=="__main__":
    a = argparse.ArgumentParser()

    a.add_argument("file", nargs="+")

    tot = a.parse_args()

    main(tot)
