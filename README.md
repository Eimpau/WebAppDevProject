# WebAppDevProject
Web Application (Factory Machinery Status &amp; Repair Tracking System)

ACME Manufacturing Corp. has contracted your software development company to build a website for them that they can use to track the operational status, repair requests and repair history for all factory machinery in their company (what they manufacture is up to you). Fortunately for you, they are a professional engineering company and know what they are looking for in a system, so as part of the procurement contract they have provided the following ideal requirements

# Requirements
- A piece of machinery can have the status "OK", "Warning", "Fault".
- If a piece of machinery breaks down, "Technicians" should be able to create a "Fault" case against it, indicating that its not working and needs to be repaired, along with notes and images about the fault. Each time a "Fault" is created, it should get its own unique case number where the history of the fault can be recorded and inspected later.
- When "Repair" personnel are working on the machine, they can add new notes and images to the "Fault" case, and if it has been fully repaired, they can mark the Fault as being resolved, returning the machine back to “OK” operational status. “Technicians” and “Managers” should be able to comment on these cases too.
- “Warnings” are free-form text string statuses that can be added to a machine. A machine has a status of “Warning” if any warnings are actively set. A machine can have multiple active “Warnings” (duplicate warning strings can be ignored). Warnings can be added by “Technicians” users (or via the API below) and removed by “Technicians” or “Repair”.
- "Managers" should see a dashboard summarizing all current machine statuses, but also the ability to drill down and view summaries for different collections of machinery.
- "Managers" should be able to generate and export file reports for groups of machinery or individual pieces of machinery.
- "Managers" can assign "Technicians" and "Repair" personnel to specific machines. When "Technicians" and "Repair" accounts view their main dashboard view, they should first see the statuses of the machines they are assigned to, but if they want they can still view the statuses of the other machines.
- More important machinery should appear first when being viewed in lists. "Managers" can add new pieces of machinery and delete old pieces of machinery.
- External monitoring systems that the customer already has should be able make a simple JSON-based HTTP POST API request to automatically record "Warnings" or "Faults" for any piece of machinery. (You should provide test forms for this piece of functionality).
- REST APIs should be provided to view current machine status (e.g. this API could be read by external systems to show system status on an operator console or using colored LEDs).
- REST APIs should exist that can list open cases, read the content of a specific case and and add a text entry to a specific case.
- A piece of machinery can be a member of multiple user-definable collections, e.g. MainCampus, Building-A, Floor-12, Room-15, Soldering-Machines, Model-53A. Collections are “flat”, i.e. they only contain machines and no other nested collections. Collection names should match the regex [A-Za-z0-9\-].

# Data Visualisation/Summarisation/Dashboard:
To present the current and historical machine statuses in a way that is easy to understand for the user at a glance, you should create summary visualizations. A few examples for visualisation can be taken from the Javascript Graphics Section on the W3Schools Website accessible at: https://www.w3schools.com/js/js_graphics.asp The most important JavaScript libraries for graphs and visualisation are Plotly.js, Chart.js, D3.js and Google Chart.

# User Authentication and User Access Roles: 
You are expected to implement an authentication mechanism for your group application. The different possible roles of users are “Technician”, “Repair”, “Managers” and “View-only”. Only “Managers” should be able to create or delete accounts.

# User Manual: 
A user guide should be included with the product, detailing what the website does and how it can be used. This will be read by each of the different kinds of users describe above, along with IT staff who will be maintaining the site.
