import os
import subprocess
import argparse
import string


USED_NERD_ICONS = [
  '\ue73c', '\ue736', '\ue749', '\ue738', '\ue83e', # Projects icons
  '\uf465' # Quote source icon
]


def unicode_list_to_unicodes_arg(chars):
  return ",".join(f"U+{ord(c):04X}" for c in chars)


def subset_font(font_path, output_path):
  """
  Use pyftsubset to generate a minimized .woff2 font containing only defined unicode ranges and symbols.
  """

  nerd_icons = unicode_list_to_unicodes_arg(USED_NERD_ICONS)
  unicode_ranges = (
    "U+0000-007F,"  # Basic Latin
    "U+0080-00FF,"  # Latin-1 Supplement
    "U+0100-017F,"  # Latin Extended-A
    "U+2500-257F,"  # Box Drawing
  )
  # Cheat sheet: https://htmlescape.net/unicode_charts.html

  unicodes_arg = "--unicodes=" + unicode_ranges + nerd_icons

  cmd = [
    "pyftsubset",
    font_path,
    f"--output-file={output_path}",
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
    "--drop-tables=FFTM,STAT,DSIG,PfEd",
    unicodes_arg
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

  print("[*] Subsetting fonts...")
  for filename in os.listdir(args.fonts_dir):
    if filename.lower().endswith(".ttf"):
      font_path = os.path.join(args.fonts_dir, filename)

      out_path = os.path.join(
        args.output_dir,
        os.path.splitext(filename)[0] + ".woff2"
      )

      subset_font(font_path, out_path)

  print("Done!\n")


if __name__ == "__main__":
  main()
