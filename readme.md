# Library Management System 

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
 
### Authentication:
For authentication, jwt authentication is used.


