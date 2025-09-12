#!/usr/bin/env python
"""
Script para verificar y crear membresías activas en la base de datos.
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from Apps.workspace.models import Organization, Project, Membership
from Apps.modeling.models import Diagram
from django.contrib.auth.models import User

def main():
    print('=== VERIFICANDO DATOS DE PRUEBA ===')
    
    # Verificar usuarios
    print('\n=== USUARIOS ===')
    users = User.objects.all()
    for user in users:
        print(f'Usuario: {user.username} (ID: {user.id})')
    
    if not users.exists():
        print('❌ No hay usuarios. Creando usuario de prueba...')
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        print(f'✅ Usuario creado: {user.username}')
    else:
        user = users.first()
    
    # Verificar organizaciones
    print('\n=== ORGANIZACIONES ===')
    orgs = Organization.objects.all()
    for org in orgs:
        print(f'Org: {org.name} (ID: {org.id})')
    
    if not orgs.exists():
        print('❌ No hay organizaciones')
        return
    else:
        org = orgs.first()
    
    # Verificar membresías
    print('\n=== MEMBRESÍAS ===')
    memberships = Membership.objects.all()
    for membership in memberships:
        print(f'Usuario: {membership.user.username} -> Org: {membership.organization.name} (Status: {membership.status})')
    
    # Crear membresía activa si no existe
    if not memberships.filter(user=user, organization=org, status='active').exists():
        print('❌ No hay membresía activa. Creando...')
        membership = Membership.objects.create(
            user=user,
            organization=org,
            role='admin',
            status='active'
        )
        print(f'✅ Membresía creada: {user.username} -> {org.name}')
    
    # Verificar proyectos
    print('\n=== PROYECTOS ===')
    projects = Project.objects.all()
    for project in projects:
        print(f'Proyecto: {project.name} -> Org: {project.organization.name} (ID: {project.id})')
    
    # Verificar diagramas
    print('\n=== DIAGRAMAS ===')
    diagrams = Diagram.objects.all()
    for diagram in diagrams:
        print(f'Diagrama: {diagram.name} -> Proyecto: {diagram.project.name} (ID: {diagram.id})')
    
    # Crear diagrama si no existe
    if not diagrams.exists() and projects.exists():
        print('❌ No hay diagramas. Creando diagrama de prueba...')
        project = projects.first()
        diagram = Diagram.objects.create(
            name='Test Diagram',
            project=project,
            created_by=user,
            type='class',
            content='{"classes": [], "relations": []}'
        )
        print(f'✅ Diagrama creado: {diagram.name}')
    
    print('\n=== DATOS DE PRUEBA LISTOS ===')
    if diagrams.exists():
        diagram = diagrams.first()
        print(f'Puedes probar con diagram_id: {diagram.id}')

if __name__ == '__main__':
    main()