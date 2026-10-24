# Django SOC Platform 🛡️

A Django-based Security Operations Center (SOC) platform for managing security alerts, coordinating incident response, enforcing role-based access control, and monitoring incident activity in real time.

## ✨ Features

- **Security Alert Management** — Track security alerts and their statuses throughout the investigation lifecycle.
- **Incident Management** — Create, assign, manage, and resolve security incidents.
- **Role-Based Access Control** — Separate permissions for SOC Analysts and SOC Leads.
- **Incident Ownership** — Allow analysts to claim unassigned incidents, unassign themselves, and resolve incidents they own.
- **Incident Reassignment** — Enable SOC Leads to reassign and resolve incidents across the team.
- **Resolution Safeguards** — Prevent incident resolution while linked alerts remain `OPEN` or `IN_PROGRESS`.
- **Append-Only Audit Logging** — Maintain a traceable record of incident changes and protect existing audit records against modification and deletion.
- **Real-Time Dashboard** — Deliver live incident-count updates through WebSockets.
- **WebSocket Authentication** — Authenticate WebSocket connections.
- **Secure API Authorization** — Enforce permissions on sensitive incident operations and restrict generic incident updates and deletions to authorized SOC Leads.

## 🛠️ Tech Stack

- Python
- Django
- Django REST Framework
- Django Channels
- WebSockets
- Git and GitHub

## 🔐 Role-Based Access Control

| Capability | SOC Analyst | SOC Lead |
|---|---|---|
| Claim unassigned incidents | ✅ | Subject to configured permissions |
| Unassign own incidents | ✅ | Subject to configured permissions |
| Resolve own incidents | ✅ | ✅ |
| Reassign any incident | ❌ | ✅ |
| Resolve any incident | ❌ | ✅ |
| Generic incident updates and deletion | ❌ | ✅ |

All protected operations are authorized on the backend. Incident resolution is blocked while any linked alert remains `OPEN` or `IN_PROGRESS`.

## 🚀 Getting Started

### Prerequisites

- Python 3
- Git
- pip

### Installation

```bash
git clone https://github.com/frenkiegithua/django-soc-project.git
cd django-soc-project

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Configure the required environment variables, then initialize the database and SOC roles:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py setup_soc_roles
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

### Run Tests

```bash
python manage.py test
```

## 🧠 Key Engineering Concepts

- Role-based and ownership-based authorization.
- Secure REST API design.
- Incident lifecycle and state-transition validation.
- Append-only audit trails.
- Real-time event delivery using WebSockets.
- WebSocket authentication and connection recovery.
- Separation of authorization rules from dashboard presentation.

## 👨‍💻 Author

**Francis Githua**

Computer Science | Networking | Cybersecurity | Security Operations

- GitHub: [@frenkiegithua](https://github.com/frenkiegithua)
- Portfolio: [francisgithua.netlify.app](https://francisgithua.netlify.app)

---

*Developed as a practical cybersecurity engineering project focused on SOC workflows, incident management, and secure backend development.*
