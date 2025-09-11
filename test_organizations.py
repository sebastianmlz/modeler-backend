#!/usr/bin/env python3
"""
Test script para endpoints de Workspace - Organizations (W01, W02, W03)
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

def test_w01_create_organization():
    """W01 - Crear organización"""
    print("🏢 Testing W01 - Crear organización...")
    
    headers = get_auth_headers()
    if not headers:
        return None
    
    payload = {
        "name": "Acme Corporation",
        "slug": "acme-corp"
    }
    
    response = requests.post(f"{BASE_URL}/organizations/", 
                           json=payload, 
                           headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        return response.json().get('id')
    return None

def test_w01_duplicate_slug():
    """W01 - Test slug duplicado (debe dar error 400)"""
    print("\n❌ Testing W01 - Slug duplicado...")
    
    headers = get_auth_headers()
    if not headers:
        return
    
    payload = {
        "name": "Another Acme",
        "slug": "acme-corp"  # Mismo slug que antes
    }
    
    response = requests.post(f"{BASE_URL}/organizations/", 
                           json=payload, 
                           headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_w02_list_organizations():
    """W02 - Listar mis organizaciones"""
    print("\n📋 Testing W02 - Listar organizaciones...")
    
    headers = get_auth_headers()
    if not headers:
        return
    
    response = requests.get(f"{BASE_URL}/organizations/", headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_w02_search_organizations():
    """W02 - Buscar organizaciones"""
    print("\n🔍 Testing W02 - Buscar organizaciones...")
    
    headers = get_auth_headers()
    if not headers:
        return
    
    response = requests.get(f"{BASE_URL}/organizations/?search=Acme", headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_w03_get_organization(org_id):
    """W03 - Obtener organización por ID"""
    print(f"\n🏢 Testing W03 - Obtener organización {org_id}...")
    
    if not org_id:
        print("❌ No hay ID de organización para probar")
        return
    
    headers = get_auth_headers()
    if not headers:
        return
    
    response = requests.get(f"{BASE_URL}/organizations/{org_id}/", headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_unauthorized_access():
    """Test acceso sin autenticación"""
    print("\n🔒 Testing acceso sin autenticación...")
    
    response = requests.get(f"{BASE_URL}/organizations/")
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("🚀 Testing Organizations Endpoints (W01, W02, W03)")
    print("=" * 50)
    
    # Test W01 - Crear organización
    org_id = test_w01_create_organization()
    
    # Test W01 - Slug duplicado
    test_w01_duplicate_slug()
    
    # Test W02 - Listar organizaciones
    test_w02_list_organizations()
    
    # Test W02 - Buscar organizaciones  
    test_w02_search_organizations()
    
    # Test W03 - Obtener organización
    test_w03_get_organization(org_id)
    
    # Test acceso sin autenticación
    test_unauthorized_access()
    
    print("\n✅ Organizations tests completed!")
