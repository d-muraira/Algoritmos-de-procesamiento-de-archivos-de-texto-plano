# Text Analysis Web Application

This Django-based web application provides various text analysis tools including autocomplete, longest common substring (LCS), Knuth-Morris-Pratt (KMP) pattern matching, and Manacher's algorithm for finding the longest palindromic substring.

## Features

1. **Autocomplete**: 
   - Allows users to upload a text file and provides word suggestions as the user types.
   - Implements a Trie data structure for efficient autocomplete functionality.

2. **Longest Common Substring (LCS)**:
   - Accepts two text files as input.
   - Finds and highlights the longest common substring between the two texts.

3. **KMP Pattern Matching**:
   - Allows users to search for a pattern within a larger text.
   - Implements the Knuth-Morris-Pratt algorithm for efficient string matching.
   - Highlights all occurrences of the pattern in the text.

4. **Manacher's Algorithm**:
   - Finds the longest palindromic substring in a given text.
   - Highlights the found palindrome in the original text.

## Project Structure

- `views.py`: Contains the main logic for all features.
- `home.html`: The main page of the application.
- `autocompletar.html`: Template for the autocomplete feature.
- `lcs.html`: Template for the Longest Common Substring feature.
- `manacher.html`: Template for the Manacher's algorithm feature.

## Setup and Running

1. Ensure you have Django installed.
2. Clone this repository.
3. Navigate to the project directory.
4. Run `python manage.py runserver` to start the development server.
5. Access the application at `http://localhost:8000`.

## Usage

1. **Autocomplete**:
   - Upload a text file.
   - Start typing in the input field to see word suggestions.

2. **LCS**:
   - Upload two text files.
   - The application will find and highlight the longest common substring.

3. **KMP Search**:
   - Upload a text file or enter text directly.
   - Enter a search pattern.
   - The application will highlight all occurrences of the pattern.

4. **Manacher's Algorithm**:
   - Upload a text file.
   - The application will find and highlight the longest palindromic substring.

## Technologies Used

- Django
- HTML/CSS
- JavaScript (for autocomplete functionality)

## Note

This project is for educational purposes and demonstrates various string algorithms. It may not be optimized for large-scale use.
