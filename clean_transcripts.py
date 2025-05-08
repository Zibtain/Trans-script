import re

def clean_transcripts(text):
    # Remove timestamps
    text = re.sub(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', '', text)
    
    # Remove line numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove empty lines
    text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())
    
    return text

def main():
    file_path = input("Enter the path to the document file: ")
    
    with open(file_path, 'r') as file:
        document = file.read()
    
    cleaned_document = clean_transcripts(document)
    
    with open("cleaned_transcripts.txt", 'w') as output_file:
        output_file.write(cleaned_document)

if __name__ == "__main__":
    main()
