# DevSecOps Lab — App conteneurisée, CI/CD sécurisée & backend isolé

Lab DevSecOps complet : une application conteneurisée déployée sur une VM via
**Infrastructure as Code**, avec une **chaîne CI/CD sécurisée**, du **monitoring**,
et une **segmentation réseau** qui isole le backend du réseau public.

## Architecture

Trois réseaux Docker cloisonnés sur une seule VM :

- **edge** (public) — seul le reverse proxy y est exposé (ports 80/443)
- **backend** (`internal: true`) — application + base de données, aucune route vers Internet
- **monitoring** — Prometheus, Grafana, exporters

Double protection : le pare-feu de l'hôte (UFW) n'ouvre que 22/80/443, et la base
de données vit dans un réseau interne qui ne peut ni être atteint de l'extérieur
ni exfiltrer vers Internet.

## Stack

| Couche | Outil |
|---|---|
| IaC (config VM) | Ansible |
| IaC (provisioning, phase 2) | Terraform / OpenTofu |
| Conteneurs | Docker + Compose |
| Reverse proxy | Traefik |
| App démo | FastAPI + PostgreSQL |
| Tests | pytest |
| CI/CD | GitHub Actions |
| Sécurité pipeline | Trivy · Gitleaks · Semgrep |
| Monitoring | Prometheus + Grafana |

## Structure du repo

```
devsecops-lab/
├── infra/ansible/      # Étape 1 — socle : durcissement + Docker  ✅
├── app/                # Étape 2 — app FastAPI + Dockerfile + tests
├── deploy/             # Étape 2 — docker-compose.yml (3 réseaux isolés)
├── .github/workflows/  # Étape 3-4 — pipeline CI/CD sécurisé
├── monitoring/         # Étape 5 — Prometheus + Grafana
└── README.md
```

## Feuille de route

- [x] **Étape 1 — Socle** : Ansible installe Docker + durcit la VM
- [x] **Étape 3 — Tests + CI** : pytest + lint/test/build/scan d'image
- [ ] **Étape 4 — CD** : déploiement automatique sur la VM
- [ ] **Étape 5 — Monitoring** : Prometheus + Grafana + exporters
- [ ] **Étape 6 — Durcissement Sec** : Trivy, Gitleaks, gestion des secrets

## Démarrer l'étape 1

Prérequis : une VM Ubuntu Server 24.04 accessible en SSH avec un user `deploy`
(sudo + ta clé publique déployée), et Ansible sur ta machine.

```bash
cd infra/ansible
ansible-galaxy collection install -r requirements.yml   # installe community.general
# édite inventory.ini : remplace CHANGE_ME_IP par l'IP de ta VM
ansible-playbook site.yml --check    # dry-run : montre ce qui changerait
ansible-playbook site.yml            # applique pour de vrai
```

> ⚠️ Le rôle `hardening` désactive l'authentification SSH par mot de passe.
> Vérifie que ta clé SSH fonctionne **avant** de lancer, sinon tu perds l'accès.

## Critères de réussite (étape 1)

- [ ] `ansible-playbook site.yml` passe sans erreur (idempotent : un 2e run ne change rien)
- [ ] `sudo ufw status` ne montre que 22/80/443 autorisés
- [ ] `docker run hello-world` fonctionne sans `sudo`
- [ ] La connexion SSH par mot de passe est refusée, par clé acceptée
