# Olivetum

Olivetum is an e-commerce website that lists olive-based products for sale. The website fosters genuine and
locally-produced goods, to support farmers with their struggle against Xylella in Salento, Italy. See [this
article](https://www.olivami.com/en/blog/curiosities-about-olive-trees/xylella-an-unprecedented-battle/) for further
information about the context. This project collects all farmers' produce and pays them back, once their products are
successfully sold for profit. The categories may range from olive oil, tapenade, or pitted kalamata, depending on the
actual availability.

[Inserire layout multi-piattaforma]

## Table of Contents
* [User Experience Design (UX)](#User-Experience-Design)
    * [The Strategy Plane](#The-Strategy-Plane)
        * [Site Goals](#Site-Goals)
        * [Agile Planning](#Agile-Planning)
          * [User Stories](#User-Stories)
    * [The Scope Plane](#The-Scope-Plan)
    * [The Structure Plane](#The-Structure-Plan)

# User-Experience-Design

## The-Strategy-Plane

### Site-Goals

The website empowers local farmers with online presence, to let them reach a broader target, that ranges from private
customers to businesses, such as restaurants. In other words, the selling activity is meant as both B2C and B2B models.
Initially, this project gives complete authority to the owners of the website, that will mediate between providers (the
farmers) and end-customers. On a later stage, the website becomes a platform that will offer sellers' onboarding, to let
each selling account conduct their selling strategy. This will be eventually possible with Stripe Connect and related
services.

Actors on the website will be administrators, staff, sellers, and end-customers. Each account type behaves differently
on the platform. The scope of this project will grant these actors all the basic and required functions expected for the
selling activity. For example, sellers' profiles will store basic information about themselves, to show the end-user the
source of the products being purchased; there is no need to collect KYC data in this phase, as the staff will take on
this responsibility at the beginning.

### Agile Planning

This project intends to use agile methodologies, by delivering small features in incremental sprints. The time this
document was drafted, 4 sprints were mainly projected.

All issues were assigned to epics, prioritized under the labels Must have, Should have, Could have. They were assigned
to sprints and stories according to their complexity (being self-explanatory). This allowed the main requirements to be
completed first, while secondary features could be added whether time could be allocated to them or not.

The Kanban board was created using github projects and can be found ```Link to the project```. It can be viewed to see
more information on the project cards. Some stories have a set of acceptance criteria in order to define the
functionality that marks that story as complete. Some other stories do not have acceptance criteria, as they were
considered self-explanatory.

```Pic to the project overview (Kanban board)```

#### User Stories

The following user stories were completed over time. Basic setup stories - such as development-related ones - have been
omitted, to prioritize those strictly pertaining the end-user experience.

The categories of users described below are:
- "Site User" - meant as a non-authenticated user.
- "Admin" - meant as an authenticated user with admin privileges.
- "Shopper" - meant as an authenticated user whose purpose is to place and review orders.

**Customer's statement**

As the shop owners, we give local farmers the opportunity to reach a broader target, via online shopping. Shoppers will
be able to interact with the website, to manage their orders and purchasing process. The staff/owners can help in
specific scenarios, to guarantee the best CX.

**Epics**

The project can be divided into 5 Epics.

**Admin and store management**

As a site admin I can manipulate (add/edit/delete) products, so that I can handle the available listings on the website.

As a site admin I can moderate (approve/delete) product reviews, so that I can prevent bad actors from leaving malicious
or misleading information.

As a site admin I can re-stock products, so that I can let customers view available products only.

**Viewing and Navigation**

As a shopper, I can view the list of available products, so that I can select some to purchase.

As a shopper, I can view the individual product details, so that I can see the price, description, product rating,
product image, and available options such as litres and grams.

As a shopper, I can quickly identitfy deals, clearance items and special offers, so that I can take advantage of special
savings on products.

As a shopper, I can easily view the total of my purchases at any time, so that I can avoid spending too much.

**Registration and User Accounts**

As a site user, I can easily register for an account, so that I have a personal account and be able to view my profile.

As a site user, I can easily log in or log out, so that I can access my personal account information.

As a site user, I can easily recover my password in case I forget it, so that I recover access to my account.

As a site user, I can receive an email confirmation after registering, so that I verify that my account registration was
successful.

As a site user, I can have a personalised user profile, so that I view my personal order history and save my payment
information.

**Sorting and Searching**

As a shopper, I can sort the list of available products, so that I can easily identify the best-rated, best-priced, and
categorically-sorted products.

As a shopper, I can sort sort a specific category of products, so that I can easily identify the best-rated, best-priced
product in a specific category, or sort the products in that category by name.

As a shopper, I can sort multiple categories of products simultaneously, so that I can find the best-rated or
best-priced products across broad categories, such as "food" and "homeware".

As a shopper, I can search for a product by name or description, so that I can find a specific product I would like to
purchase.

As a shopper, I can search for a product by name or description, so that I can find a specific product I would like to
purchase.

As a shopper, I can easily see what I have searched for and the number of results, so that I can quickly decide whether
the product I want is available.

**Purchasing and Checkout**

As a shopper, I can easily select the size and the quantity of a product when purchasing it, so that I can ensure I do
not accidentally select the wrong product, quantity, or size.

As a shopper, I can view items in my bag to be purchased, so that I can identify the total cost of my purchase and all
items I will receive.

As a shopper, I can adjust the quantity of individual items in my bag, so that I can easily make changes to my purchase
before checkout.

As a shopper, I can easily enter my payment information, so that I can check out quickly and with no hassles.

As a shopper, I can feel my personal and payment information are safe and secure, so that I confidently provide the
needed information to make a purchase.

As a shopper, I can view an order confirmation after checkout, do that I can verify that I have not made any mistakes.

As a shopper, I can receive an email confirmation after checking out, so that I can keep the confirmation of what I have
purchased for my records.

**Documentation**

Tasks:

* Complete readme documentation
* Complete testing documentation write up

## The-Scope-Plan

* Responsive Design - Site should be fully functional on all devices from 320px up
* Hamburger menu for mobile devices
* Ability to perform CRUD functionality on products - admin
* Restricted role-based features
* Home page with grid of products
* Review of orders for shoppers
* Review of payment details for shoppers

## The-Structure-Plan

### Features

#### Colour-palette
The colour palette can be found at https://colorhunt.co/palette/181d31678983e6ddc4f0e9d2

```To be completed```