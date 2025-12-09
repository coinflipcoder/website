import os
import subprocess
import argparse
import string


USED_NERD_ICONS = [
  '\ue73c', '\ue736', '\ue749', '\ue738', '\ue83e', # Projects icons
  '\uf465' # Quote source icon
]

USED_EXTRA_ICONS = [
  '─', '└', '├'
]


def write_chars_file(chars, output_file):
  with open(output_file, "w", encoding="utf-8") as f:
    f.write(chars)
  print(f"[OK] Saved used character list to {output_file}")


def get_all_used_characters():
  """
  Combines:
  - String letters, digits and punctuation
  - Selected Nerd Font icons
  """
  chars = set()

  # Always include alphanumerics
  chars.update(string.ascii_letters)
  chars.update(string.punctuation)
  chars.update(string.whitespace)
  chars.update(string.digits)

  # Add extra icons
  chars.update(USED_NERD_ICONS)
  chars.update(USED_EXTRA_ICONS)

  return "".join(sorted(chars))


def subset_font(font_path, chars_file, output_path):
  """
  Use pyftsubset to generate a minimized .woff2 font containing only used chars.
  """
  cmd = [
    "pyftsubset",
    font_path,
    f"--output-file={output_path}",
    f"--text-file={chars_file}",
    "--flavor=woff2",
    "--layout-features=''",
    "--no-glyph-names",
    "--no-symbol-cmap",
    "--no-legacy-cmap",
    "--notdef-glyph",
    "--notdef-outline",
    "--no-recalc-bounds",
    "--no-hinting",
    "--desubroutinize",
    "--drop-tables=FFTM,STAT,DSIG,PfEd"
  ]

  print(f"[RUNNING] {' '.join(cmd)}")
  subprocess.run(" ".join(cmd), shell=True, check=True)
  print(f"[OK] Subset font written to {output_path}")


def main():
  parser = argparse.ArgumentParser(description="Subset Nerd Font .woff2 files for deployment")
  parser.add_argument("--fonts-dir", required=True, help="Directory containing .ttf fonts")
  parser.add_argument("--output-dir", required=True, help="Directory to write subset fonts")

  args = parser.parse_args()

  os.makedirs(args.output_dir, exist_ok=True)

  print("[*] Creating characters file...")
  chars = get_all_used_characters()

  chars_file = os.path.join(args.output_dir, "used_chars.txt")
  write_chars_file(chars, chars_file)

  print("[*] Subsetting fonts...")
  for filename in os.listdir(args.fonts_dir):
    if filename.lower().endswith(".ttf"):
      font_path = os.path.join(args.fonts_dir, filename)

      out_path = os.path.join(
        args.output_dir,
        os.path.splitext(filename)[0] + ".woff2"
      )

      subset_font(font_path, chars_file, out_path)

  print("Done!\n")


if __name__ == "__main__":
  main()
