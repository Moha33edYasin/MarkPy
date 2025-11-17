Hello, here is a markup lang with your style.  
Type your settings in the settings file in the following format:  
[1nd mark] [tag] [2nd mark] [3rd mark] [4th mark] [key]  
**Notes**:  
    - [1st mark] is required for any token.  
    - [tag] is required HTML element that holds the 1st and 2nd tokens.  
    - [2nd mark] is for any additional enclosed markers you want to add.  
    - [3rd and 4th marks] are optional enclosed tokens that provide extra information for the HTML tag (such as links, images, ...etc).  
    - [key] is any html args that holds 3rd and 4th token.  
    - Don't forget spearate your arguments with spaces.  
      *Examples*:  
          1. # h (means '#Title' is a header of type 1)  
          2. ** b ** (means '**text**' is a bold text)  
          3. [ a ] ( ) href (means '[link name](url)' is a link)  
    - To change static marks (pragraph mark and line break mark), go to __init__.py.  
    - The module is indent-sensitive, which is used to determine elements belong block.  
    - 1 indent = 4 spaces.  
    - look at demo.py and demo.txt files if want a concrete example.  
