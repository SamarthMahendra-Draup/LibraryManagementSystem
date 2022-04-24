# Library Management System 
***
___
## Description :
This project contains all the necessary api used in library management system. The api's in the project is created using django restframework and database as postgres.

Contains Following api's:
 * Users 
   * Viewall
   * Viewone (by id)
   * Add user 
   * Update user
   * Delele user (by id)
 * Books
    * Viewall
    * Viewone (by id)
    * Add book
    * Update book
    * Delete book(by id)
 * Books log
    * Viewall
    * ViewOne
    * Add book log
    * Update ( update return date)
    * Delete
 * Role - (admin / librarian / teacher / student)
   * Viewall
   * Viewone
   * Add 
   * Update
   * Delete
 * Caluclate fee

Books log stores user id and book id and isuued date and expected returned date and user returned date, so based on number of days borrowed, fee is calculated.

***
 
### Authentication:
For authentication, jwt authentication is used.

---

For users 
* Viewall :
  * Just pass your jwt auth token and if you have permission to see the users.
    You will be returned with all the users
* Viewone :
  * Pass the id in the url like viewone/id 
* Add :
  * pass in your token and json object  in format 
  
    ```javascript
    {
        "username" : ".....",
        "password" : ".....",
        "email" : ".....",
        "first_name" : ".....",
        "last_name" : ".....", 
        "role" : "....."
    } 
    ```

* Update :
  * pass in your token and json object  in format 
  
    ```javascript
    {
        "username" : ".....",
        "password" : ".....",
        "email" : ".....",
        "first_name" : ".....",
        "last_name" : "....." 
        "role" : "....."
    } 
    ```
    
* Delete :
  * Pass the id in the url like delete/id 

***
For Books :
 * Viewall 
    * Any one can view the books no need of token
 * Viewone
    * Any one can view a book
 * Add 
    * You need to be a librarian to add a book and it should be in 
     the format of 
      ```javascript
      {
        "book_id": "6",
        "book_title": "Harry Potter and the Deathly hallows part 1",
        "author": "J.K rouling"
      }
      ```
 * Update
    * You need to be a librarian to update a book and it should be in 
     the format of 
      ```javascript
      {
        "book_id": "6",
        "book_title": "Harry Potter and the Deathly hallows part 1",
        "author": "J.K rouling"
      }
      ```
* Delete 
    * You need to be a librarian to delete a book by id 
 ***

For Book_log
 * you need to be a librarian to acess this api

 * Viewall 
    * Pass in your auth token and you will get all book logs
 * Viewone 
    * Pass in your auth token and id of log , corresponding log will be returned
 * Add
      * ```javascript
        {
        "user_id":2,
        "book_id":1,
        "date_issued":"2022-04-22",
        "date_exp":"2022-04-24"
        }
      ```
        
 * Update
    * You can only update the returned date
   
     format: 
    ```javascript
        {
        "date_returned":"2022-04-28"
        }
    ```
 * Delete 
    * You can delete log by id 
          
      
    
    



