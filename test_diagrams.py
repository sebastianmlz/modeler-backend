#!/usr/bin/env python3
"""
Test script para endpoints de Modeling - Diagrams (M01, M02, M03)
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

def get_project_id():
    """Obtener ID de un proyecto existente."""
    headers = get_auth_headers()
    if not headers:
        return None
    
    # Primero obtener una organización
    orgs_response = requests.get(f"{BASE_URL}/organizations/", headers=headers)
    if orgs_response.status_code != 200:
        print("❌ Error al obtener organizaciones")
        return None
    
    orgs = orgs_response.json().get('results', [])
    if not orgs:
        print("❌ No hay organizaciones disponibles")
        return None
    
    org_id = orgs[0]['id']
    
    # Obtener proyectos de esa organización
    projects_response = requests.get(f"{BASE_URL}/projects/?organization={org_id}", headers=headers)
    
    if projects_response.status_code == 200:
        projects = projects_response.json().get('results', [])
        if projects:
            return projects[0]['id']
        else:
            print("❌ No hay proyectos disponibles")
            return None
    else:
        print(f"❌ Error al obtener proyectos: {projects_response.status_code}")
        return None

def test_m01_create_diagram(project_id):
    """M01 - Crear diagrama"""
    print("📊 Testing M01 - Crear diagrama...")
    
    if not project_id:
        print("❌ No hay proyecto para crear el diagrama")
        return None
    
    headers = get_auth_headers()
    if not headers:
        return None
    
    payload = {
        "project": project_id,
        "name": "Initial diagram"
    }
    
    response = requests.post(f"{BASE_URL}/diagrams/", 
                           json=payload, 
                           headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        return response.json().get('id')
    return None

def test_m01_duplicate_name(project_id):
    """M01 - Test nombre duplicado (debe dar error 400)"""
    print("\n❌ Testing M01 - Nombre duplicado...")
    
    if not project_id:
        print("❌ No hay proyecto para probar")
        return
    
    headers = get_auth_headers()
    if not headers:
        return
    
    payload = {
        "project": project_id,
        "name": "Initial diagram"  # Mismo nombre que antes
    }
    
    response = requests.post(f"{BASE_URL}/diagrams/", 
                           json=payload, 
                           headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_m02_list_diagrams(project_id):
    """M02 - Listar diagramas del proyecto"""
    print(f"\n📋 Testing M02 - Listar diagramas del proyecto {project_id}...")
    
    if not project_id:
        print("❌ No hay proyecto para listar diagramas")
        return
    
    headers = get_auth_headers()
    if not headers:
        return
    
    response = requests.get(f"{BASE_URL}/diagrams/?project={project_id}", headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_m02_missing_project():
    """M02 - Test sin parámetro project (debe dar error 400)"""
    print("\n❌ Testing M02 - Sin parámetro project...")
    
    headers = get_auth_headers()
    if not headers:
        return
    
    response = requests.get(f"{BASE_URL}/diagrams/", headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_m03_get_diagram(diagram_id):
    """M03 - Obtener diagrama por ID"""
    print(f"\n📊 Testing M03 - Obtener diagrama {diagram_id}...")
    
    if not diagram_id:
        print("❌ No hay ID de diagrama para probar")
        return
    
    headers = get_auth_headers()
    if not headers:
        return
    
    response = requests.get(f"{BASE_URL}/diagrams/{diagram_id}/", headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_m03_rename_diagram(diagram_id):
    """M03 - Renombrar diagrama"""
    print(f"\n✏️ Testing M03 - Renombrar diagrama {diagram_id}...")
    
    if not diagram_id:
        print("❌ No hay ID de diagrama para probar")
        return
    
    headers = get_auth_headers()
    if not headers:
        return
    
    payload = {
        "name": "Renamed diagram"
    }
    
    response = requests.patch(f"{BASE_URL}/diagrams/{diagram_id}/", 
                            json=payload, 
                            headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_m03_delete_diagram(diagram_id):
    """M03 - Eliminar diagrama (soft delete)"""
    print(f"\n🗑️ Testing M03 - Eliminar diagrama {diagram_id}...")
    
    if not diagram_id:
        print("❌ No hay ID de diagrama para probar")
        return
    
    headers = get_auth_headers()
    if not headers:
        return
    
    response = requests.delete(f"{BASE_URL}/diagrams/{diagram_id}/", headers=headers)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 204:
        print("✅ Diagrama eliminado exitosamente")
    else:
        print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_unauthorized_access():
    """Test acceso sin autenticación"""
    print("\n🔒 Testing acceso sin autenticación...")
    
    response = requests.get(f"{BASE_URL}/diagrams/")
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("🚀 Testing Diagrams Endpoints (M01, M02, M03)")
    print("=" * 50)
    
    # Obtener proyecto para los tests
    project_id = get_project_id()
    print(f"📁 Usando proyecto: {project_id}")
    
    # Test M01 - Crear diagrama
    diagram_id = test_m01_create_diagram(project_id)
    
    # Test M01 - Nombre duplicado
    test_m01_duplicate_name(project_id)
    
    # Test M02 - Listar diagramas del proyecto
    test_m02_list_diagrams(project_id)
    
    # Test M02 - Sin parámetro project
    test_m02_missing_project()
    
    # Test M03 - Obtener diagrama
    test_m03_get_diagram(diagram_id)
    
    # Test M03 - Renombrar diagrama
    test_m03_rename_diagram(diagram_id)
    
    # Test M03 - Eliminar diagrama
    test_m03_delete_diagram(diagram_id)
    
    # Test acceso sin autenticación
    test_unauthorized_access()
    
    print("\n✅ Diagrams tests completed!")