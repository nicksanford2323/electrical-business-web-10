import os

def combine_specific_files():
    # List of files to combine based on the screenshot
    files_to_combine = [
        'LoadingScreen.jsx',
        'LoadingScreen.css',
        'Reviews.jsx',
        'Reviews.css',
        'ServiceArea.jsx',
        'ServiceArea.css',
        'Services.jsx',
        'Services.css',
        'App.css',
        'App.jsx',
        'index.css',
        'index.jsx'
    ]

    combined_content = "// Combined React Project Files\n\n"

    # Working directory - assumes we're in the project root
    src_dir = './src'
    components_dir = os.path.join(src_dir, 'components')

    for filename in files_to_combine:
        # Try both in src and components directory
        file_paths = [
            os.path.join(src_dir, filename),
            os.path.join(components_dir, filename)
        ]

        for file_path in file_paths:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        combined_content += f"\n// {filename}\n"
                        combined_content += "".join(["=" * 50, "\n"])
                        combined_content += file.read()
                        combined_content += "\n\n"
                    print(f"Added {filename}")
                    break
                except Exception as e:
                    print(f"Error reading {filename}: {e}")

    # Write combined content to file
    try:
        with open('combined_specific_files.txt', 'w', encoding='utf-8') as f:
            f.write(combined_content)
        print("\nSuccessfully combined files into combined_specific_files.txt")
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    combine_specific_files()