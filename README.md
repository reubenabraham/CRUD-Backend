# Mock Strava - CRUD-Backend

This repository is a fully functional backend for a [Strava](https://www.strava.com/about)-like social media platform. Users can create accounts, log-in securely and create, update and 
delete posts. Then can also upvote posts by other users on their feed. 

## Usage Instructions
* Go to [Mock Strava](https://fastapi-reuben.herokuapp.com/docs)
* Scroll down to the Create User endpoint, click **Try it Out** and provide an email and password.
* Once the user is created, scroll to the top-right of the page and click on the **Authorize** icon. Enter your registered email and password and click on Authorize. This application uses JWT token authentication, so your token expires every 30 minutes.
* Once authenticated, the user is free to use all end-points - view all posts, create posts, get a post with a specific ID, etc. 
* Users can only Update and Delete their own posts.
* Users are free to vote on anyone's posts. The user must provide a post_id and a vote direction: 1 for upvote, 0 for downvote. A user may not upvote more than once, and likewise with downvotes. The post can either be upvoted or not.
