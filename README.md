# Fancy Restaurant Reservation System

## Project Outline

Fancy Restaurant Reservation System is a web application that allows users to reserve a table at a restaurant.

Users can enter the number of guests, choose a desired date and time slot, and confirm a reservation. The system assigns a suitable available table based on the number of guests. If no table is available for the selected time slot, the system suggests another nearby time slot or another nearby date.

## Main User Actions

- The user can log in or enter their name.
- The user enters the number of guests.
- The user chooses a desired date from the calendar.
- The user chooses a desired time slot.
- The user confirms the booking with an OK button.
- The user can register as a user and log in.

## Main Data Entities

- User
- Table
- Reservation
- Time Slot

## Basic Data Model Idea

- Users use Django's built-in authentication model for login information.
- Tables have a unique table number, seating capacity, and active status.
- Time slots represent reusable available reservation start times, duration, and active status.
- Reservations store an optional logged-in user, customer name, date, time slot, number of guests, assigned table, status, and timestamps.

The system should choose the smallest available table that can fit the number of guests.

The database prevents double-booking by requiring each assigned table to be unique for the same reservation date and time slot.

## Initial Database Schema

The `reservations` app defines these Django models:

- `Table`: restaurant table records ordered by capacity and table number so later booking logic can find the smallest suitable table first.
- `TimeSlot`: reusable reservation start times such as `18:00` or `19:30`.
- `Reservation`: date-specific bookings connected to a time slot and assigned table.

Each model implements `__str__()` so records are readable in Django admin.

## Main User Flow

1. The user can log in or enter their name.
2. The user enters the number of guests.
3. The user selects a date.
4. The user selects a time slot.
5. The user pushes the OK button.
6. The system looks for an available table.
7. The system assigns a suitable table to the reservation.
8. The system shows a success message and reservation details.
9. If there is no available table for the selected time slot, the system suggests another nearby time slot or another nearby date.

## User Interface Notes

- The main screen shows a reservation form.
- The user enters the number of guests, selects a date and time slot, and presses the OK button.
- After the reservation is completed, the system shows the reservation details.
- If a reservation for the desired time slot is not possible, the system suggests the closest available time slot on the selected day or notifies the user that the day is fully booked.

## Development Environment

- Python 3.10.4
- uv
- Git
- GitHub

## Tools Used

- Black: code formatter
- Pylint: linter
- Pytest: testing framework
- Coverage.py: test coverage tool

## Setup

Install dependencies using uv.

```bash
uv sync
uv run python manage.py check
uv run python manage.py makemigrations reservations
uv run python manage.py migrate
uv run python manage.py test reservations
uv run pytest
```
