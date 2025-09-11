#!/usr/bin/env python3
"""
Test script para endpoints de Workspace - Projects (W04, W05, W06)
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def get_auth_headers():
    """Obtener headers de autenticación."""
    # Primero hacer login para obtener el token
    login_response = requests.post(f"{BASE_URL}/auth/token/", json={
        "username": "admin",
        "password": "admin123"
    })
    
    if login_response.status_code == 200:
        token = login_response.json().get('access')
        return {'Authorization': f'Bearer {token}'}
    else:
        print(f"❌ Error en login: {login_response.status_code}")
        print(f"Response: {login_response.json()}")
        return None

def get_organization_id():
    """Obtener ID de una organización existente."""
    headers = get_auth_headers()
    if not headers:
        return None
    
    response = requests.get(f"{BASE_URL}/organizations/", headers=headers)
    
    if response.status_code == 200:
        orgs = response.json().get('results', [])
        if orgs:
            return orgs[0]['id']
        else:
            print("❌ No hay organizaciones disponibles")
            return None
    else:
        print(f"❌ Error al obtener organizaciones: {response.status_code}")
        return None

def test_w04_create_project(org_id):
    """W04 - Crear proyecto"""
    print("📁 Testing W04 - Crear proyecto...")
    
    if not org_id:
        print("❌ No hay organización para crear el proyecto")
        return None
    
    headers = get_auth_headers()
    if not headers:
        return None
    
    payload = {
        "organization": org_id,
        "name": "Modeler",
        "key": "MOD",
        "is_private": False
    }
    
    response = requests.post(f"{BASE_URL}/projects/", 
                           json=payload, 
                           headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        return response.json().get('id')
    return None

def test_w04_duplicate_key(org_id):
    """W04 - Test clave duplicada (debe dar error 400)"""
    print("\n❌ Testing W04 - Clave duplicada...")
    
    if not org_id:
        print("❌ No hay organización para probar")
        return
    
    headers = get_auth_headers()
    if not headers:
        return
    
    payload = {
        "organization": org_id,
        "name": "Another Modeler",
        "key": "MOD",  # Misma clave que antes
        "is_private": True
    }
    
    response = requests.post(f"{BASE_URL}/projects/", 
                           json=payload, 
                           headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_w05_list_projects(org_id):
    """W05 - Listar proyectos de una organización"""
    print(f"\n📋 Testing W05 - Listar proyectos de organización {org_id}...")
    
    if not org_id:
        print("❌ No hay organización para listar proyectos")
        return
    
    headers = get_auth_headers()
    if not headers:
        return
    
    response = requests.get(f"{BASE_URL}/projects/?organization={org_id}", headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_w05_missing_organization():
    """W05 - Test sin parámetro organization (debe dar error 400)"""
    print("\n❌ Testing W05 - Sin parámetro organization...")
    
    headers = get_auth_headers()
    if not headers:
        return
    
    response = requests.get(f"{BASE_URL}/projects/", headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_w06_get_project(project_id):
    """W06 - Obtener proyecto por ID"""
    print(f"\n📁 Testing W06 - Obtener proyecto {project_id}...")
    
    if not project_id:
        print("❌ No hay ID de proyecto para probar")
        return
    
    headers = get_auth_headers()
    if not headers:
        return
    
    response = requests.get(f"{BASE_URL}/projects/{project_id}/", headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_unauthorized_access():
    """Test acceso sin autenticación"""
    print("\n🔒 Testing acceso sin autenticación...")
    
    response = requests.get(f"{BASE_URL}/projects/")
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("🚀 Testing Projects Endpoints (W04, W05, W06)")
    print("=" * 50)
    
    # Obtener organización para los tests
    org_id = get_organization_id()
    print(f"📋 Usando organización: {org_id}")
    
    # Test W04 - Crear proyecto
    project_id = test_w04_create_project(org_id)
    
    # Test W04 - Clave duplicada
    test_w04_duplicate_key(org_id)
    
    # Test W05 - Listar proyectos de la organización
    test_w05_list_projects(org_id)
    
    # Test W05 - Sin parámetro organization
    test_w05_missing_organization()
    
    # Test W06 - Obtener proyecto
    test_w06_get_project(project_id)
    
    # Test acceso sin autenticación
    test_unauthorized_access()
    
    print("\n✅ Projects tests completed!")
