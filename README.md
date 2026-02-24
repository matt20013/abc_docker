# ABC Docker

Docker image including tools to work with ABC music notation.

This image contains:
- `abcm2ps`: For converting ABC to PostScript/PDF.
- `abcmidi`: For converting ABC to MIDI.
- `timidity`: For converting MIDI to WAV.
- `lame`: For converting WAV to MP3.
- `sox`: For audio processing.
- `python3`: For running scripts.

## Getting Started

You can pull the pre-built image from Docker Hub:

```bash
docker pull matt20013/abc-docker
```

Or build it locally:

```bash
docker build . -t abc
```

## Running Locally

To run the tools, you generally need to mount your local directories containing ABC files and where you want the output files to go. The scripts inside the container expect the following directory structure by default:
- `/abcs`: Input ABC files.
- `/pdfs`: Output PDF files.
- `/mp3s`: Output MP3 files.
- `/csvs`: Output CSV files.

Start a shell in the container:

```bash
docker run -it \
  -v ${PWD}/abcs:/abcs \
  -v ${PWD}/mp3s:/mp3s \
  -v ${PWD}/pdfs:/pdfs \
  -v ${PWD}/csvs:/csvs \
  abc bash
```

### Scripts

The container includes several scripts in the `/scripts` directory (which is the default working directory).

#### 1. Create PDF (`create_pdf.sh`)

Creates a PDF for a single ABC file.

**Usage:**

Set the `ABC_FILENAME` environment variable to the filename (without extension).

```bash
export ABC_FILENAME=tunes
./create_pdf.sh
```

**Environment Variables:**
- `ABC_FILENAME`: (Required) The name of the ABC file without extension (e.g., `tunes` for `tunes.abc`).
- `ABC_DIR`: Directory containing ABC files (default: `/abcs`).
- `PDF_DIR`: Directory for output PDFs (default: `/pdfs`).

#### 2. Generate MP3 (`generate_mp3.py`)

Generates MP3 files for each tune in an ABC file.

**Usage:**

```bash
python generate_mp3.py <input_abc_path> <output_folder>
```

**Example:**

```bash
python generate_mp3.py ../abcs/tunes.abc ../mp3s
```

#### 3. Generate CSV (`generate_csv.py`)

Generates a CSV file containing metadata for tunes in an ABC file.

**Usage:**

```bash
python generate_csv.py <input_abc_path> <output_csv_path>
```

**Example:**

```bash
python generate_csv.py ../abcs/tunes.abc ../csvs/tunes.csv
```

#### 4. Convert JPG to EPS (`convert_jpg_to_eps.sh`)

Converts all JPG files in the `/abcs` directory to EPS files in the same directory. This is useful for including images in ABC files that are processed by tools expecting EPS.

**Usage:**

```bash
./convert_jpg_to_eps.sh
```

### Batch Processing

There are helper scripts to process all ABC files in the `/abcs` directory

- **Create all PDFs:**
  ```bash
  ./create_all_pdfs.sh
  ```

- **Generate all MP3s:**
  ```bash
  ./generate_all_mp3s.sh
  ```

- **Generate all CSVs:**
  ```bash
  ./generate_all_csvs.sh
  ```

### Clean up ABC files
Fixes Windows line endings (CRLF) and trailing spaces that cause `abc2midi` to crash.
`docker run -it -v ${PWD}/abcs:/abcs/ abc ./clean_abc.sh ../abcs/tunes.abc`.

## CI / GitHub Actions

You can use this Docker image in your CI/CD pipeline to automatically generate media files from your ABC files.

Below is an example GitHub Actions workflow (`.github/workflows/generate-media.yml`) that generates PDFs and MP3s on every push to the `master` branch.

```yaml
name: Generate Media

on:
  push:
    branches: [ "master" ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Code
      uses: actions/checkout@v3

    - name: Create Output Directories
      run: mkdir -p pdfs mp3s csvs

    - name: Generate Media
      run: |
        docker run --rm \
          -v ${{ github.workspace }}/abcs:/abcs \
          -v ${{ github.workspace }}/pdfs:/pdfs \
          -v ${{ github.workspace }}/mp3s:/mp3s \
          -v ${{ github.workspace }}/csvs:/csvs \
          matt20013/abc-docker \
          bash -c "cd /scripts && ./create_all_pdfs.sh && ./generate_all_mp3s.sh"

    - name: Upload Artifacts
      uses: actions/upload-artifact@v3
      with:
        name: media-files
        path: |
          pdfs/
          mp3s/
```

This workflow:
1.  Checks out your repository (assuming your ABC files are in an `abcs` folder in the repo root).
2.  Creates output directories.
3.  Runs the Docker container, mounting the relevant directories.
4.  Executes the batch processing scripts inside the container.
5.  Uploads the generated PDFs and MP3s as build artifacts.

## Acknowledgements

This project makes use of the following tools and resources:

*   **[abcmidi](https://github.com/sshlien/abcmidi)**: For converting ABC to MIDI.
*   **[abcm2ps](http://moinejf.free.fr/)**: For converting ABC to PostScript/PDF.
*   **[TiMidity++](http://timidity.sourceforge.net/)**: For converting MIDI to WAV.
*   **[LAME](https://lame.sourceforge.io/)**: For converting WAV to MP3.
*   **[SoX](http://sox.sourceforge.net/)**: For audio processing.
*   **[ImageMagick](https://imagemagick.org/)**: For image conversion.
*   **[Ubuntu](https://ubuntu.com/)**: Base image for the container.

### Fonts and Soundfonts

*   **[Petaluma Font](https://github.com/steinbergmedia/petaluma)**: Used for music notation (SIL Open Font License).
*   **[Upright Piano KW Soundfont](https://freepats.zenvoid.org/Piano/acoustic-grand-piano.html)**: Used for MIDI playback (CC0 1.0).
