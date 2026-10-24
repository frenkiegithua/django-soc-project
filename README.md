# Django SOC Platform 🛡️

A Security Operations Center (SOC) platform built with Django to manage security alerts, track incidents, enforce role-based access control, and monitor incident activity in real time.

🚧 **Status:** In Development

## ✨ Features

- **Alert Management** — Manage security alerts and track their statuses.
- **Incident Management** — Create, assign, investigate, and resolve incidents.
- **Role-Based Access Control** — Separate permissions for SOC Analysts and SOC Leads.
- **Incident Ownership** — Analysts can claim unassigned incidents and resolve incidents assigned to them.
- **Resolution Safeguards** — Prevent incident resolution while linked alerts remain open or in progress.
- **Audit Logging** — Maintain an append-only record of incident changes.
- **Real-Time Dashboard** — Push live incident-count updates using WebSockets.
- **WebSocket Authentication** — Protect real-time connections with authentication.
- **Secure API Operations** — Enforce permissions on sensitive incident updates and deletion.

## 🛠️ Tech Stack

- Python
- Django
- Django REST Framework
- Django Channels
- WebSockets
- Git & GitHub

## 🔐 Access Control

| Capability | SOC Analyst | SOC Lead |
|---|---|---|
| Claim unassigned incidents | ✅ | Depends on configured permissions |
| Unassign own incidents | ✅ | Depends on configured permissions |
| Resolve own incidents | ✅ | ✅ |
| Reassign any incident | ❌ | ✅ |
| Resolve any incident | ❌ | ✅ |
| Generic incident updates/deletion | ❌ | ✅ |

Incident resolution is blocked while linked alerts remain `OPEN` or `IN_PROGRESS`. Authorization is enforced on the backend, not just in the user interface.

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

Configure the environment variables required by the project, then run:

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

## 📈 Development Progress

The project is being developed incrementally, with a focus on practical cybersecurity engineering and secure backend development.

Recent milestones:

- **Day 13:** WebSocket authentication and reconnection improvements.
- **Day 14:** Real-time dashboard incident counts.
- **Day 16:** Append-only incident audit logging.
- **Day 17:** SOC Analyst and SOC Lead permissions and incident ownership rules.

See [`PROGRESS.md`](PROGRESS.md) for development updates.

## 🎯 Learning Objectives

- Security alert triage and incident response workflows.
- Role-based and object-level authorization.
- Secure REST API development.
- Real-time communication with WebSockets.
- Audit logging and accountability.
- Backend security testing.

## 👨‍💻 Author

**Francis Githua**

Computer Science student | Networking | Cybersecurity | Security Operations

- GitHub: [@frenkiegithua](https://github.com/frenkiegithua)
- Portfolio: [francisgithua.netlify.app](https://francisgithua.netlify.app)

---

*Built as a hands-on project to develop practical skills in cybersecurity, SOC operations, and secure application development.*
