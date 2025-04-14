# Household Services Application

**A multi-user platform providing comprehensive home servicing solutions.**

![App Demo](https://github.com/ayushbhm/vuehousing/blob/main/merged%20(2).gif)

## 🚀 Overview

This app connects **customers**, **service professionals**, and an **admin** to manage home service requests efficiently. With an easy-to-use interface, it ensures smooth operations for booking services, assigning professionals, and managing service requests.

## 🎯 Key Features

- **Admin**: Full control to manage users, services, and approve professionals.
- **Service Professionals**: Manage service requests, accept/reject jobs, and close completed requests.
- **Customers**: Book, search, and review services, with the ability to track their requests.

## 🔧 Tech Stack

- **Backend**: Flask (API), SQLite (Data Storage), Redis (Caching)
- **Frontend**: VueJS (UI), Bootstrap (Styling)
- **Job Management**: Redis & Celery (Asynchronous Tasks)
- **Authentication**: Role-based Access Control (RBAC) using JWT 

## 💡 Functionalities

- **Admin Dashboard**: Monitor all users, manage services, and handle approvals/blocks.
- **Service Management**: Create, update, or delete services with base prices.
- **Service Requests**: Customers create, edit, or close service requests; professionals manage them.
- **Scheduled Jobs**: Daily reminders to professionals and monthly activity reports.
- **Export as CSV**: Admin can export service data via a batch job.

