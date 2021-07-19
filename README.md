# url_shortener
A small Flask app for URL shortening  
Please do the following steps to install and run it:
1. Create and activate a vitual Python enviornment for Flask.

``mkdir flask_projs``

 ``cd flask_projs``
 
``python3 -m venv venv``
 
``. venv/bin/activate``

2. Install Flask.

``pip3 install Flask``

3. Install needed python libraries.

``pip3 shortuuid``

4. Clone the repository

5. Set Flask enviorment variables. Following commands are for bash.

``export FLASK_APP=urlshortener``

6. Run Flask.

``cd urlshortener``

``flask run``

7. Type http://127.0.0.1:5000 in your browser's address bar.
8. Enter your original URL in the text box.
9. Note down the shortened URL generated.
10. Type the shortened URL in another browser tab.
11. You will be redirected to your original URL.
