#!/usr/bin/env bash
# Usage: bash scripts/archive_task.sh --slug <slug> --type <type>

SLUG=""
TYPE="feature"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --slug) SLUG="$2"; shift ;;
        --type) TYPE="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

if [ -z "$SLUG" ]; then
    echo "Error: --slug is required"
    exit 1
fi

FOLDER_TYPE="features"
if [ "$TYPE" = "cr" ]; then
    FOLDER_TYPE="cr"
elif [ "$TYPE" = "bug" ]; then
    FOLDER_TYPE="bug"
fi

# Ensure target slug directory matches prefix if type is cr or bug
if [ "$TYPE" = "cr" ] && [[ ! "$SLUG" =~ ^cr- ]]; then
    SLUG="cr-$SLUG"
elif [ "$TYPE" = "bug" ] && [[ ! "$SLUG" =~ ^bug- ]]; then
    SLUG="bug-$SLUG"
fi

echo "Archiving task '$SLUG' of type '$TYPE'..."

# Ensure archives parent folder exists
mkdir -p "second-brain/10-archives/${FOLDER_TYPE}/${SLUG}"

PHASES=(
    "03-requirements-spec"
    "04-architecture"
    "05-development"
    "06-security"
    "07-qa-testing"
)

for phase in "${PHASES[@]}"; do
    SRC_DIR="second-brain/${phase}/${FOLDER_TYPE}/${SLUG}"
    if [ -d "$SRC_DIR" ]; then
        DEST_DIR="second-brain/10-archives/${FOLDER_TYPE}/${SLUG}/${phase}"
        if [ -d "$DEST_DIR" ]; then
            echo "  [Warning] Destination $DEST_DIR already exists. Cleaning up older archive..."
            rm -rf "$DEST_DIR"
        fi
        echo "  Moving $SRC_DIR -> $DEST_DIR"
        mv "$SRC_DIR" "$DEST_DIR"
    else
        echo "  [Skip] Directory $SRC_DIR does not exist."
    fi
done

echo "Archived successfully!"
