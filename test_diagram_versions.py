#!/usr/bin/env python3
"""
Script de prueba para los endpoints de versiones de diagramas (M04, M05, M06).
"""
import requests
import json
import uuid


BASE_URL = "http://127.0.0.1:8000/api"


def get_auth_headers():
    """Obtiene headers de autenticación con JWT."""
    login_response = requests.post(f"{BASE_URL}/auth/token/", json={
        "username": "admin",
        "password": "admin123"
    })
    
    if login_response.status_code != 200:
        raise Exception(f"Error de autenticación: {login_response.text}")
    
    tokens = login_response.json()
    return {
        "Authorization": f"Bearer {tokens['access']}",
        "Content-Type": "application/json"
    }


def get_diagram_id():
    """Obtiene el ID de un diagrama existente para pruebas."""
    headers = get_auth_headers()
    
    # Obtener organización
    org_response = requests.get(f"{BASE_URL}/organizations/", headers=headers)
    if org_response.status_code != 200 or not org_response.json()['results']:
        raise Exception("No hay organizaciones disponibles")
    
    org_id = org_response.json()['results'][0]['id']
    
    # Obtener proyecto
    project_response = requests.get(f"{BASE_URL}/projects/?organization={org_id}", headers=headers)
    if project_response.status_code != 200 or not project_response.json()['results']:
        raise Exception("No hay proyectos disponibles")
    
    project_id = project_response.json()['results'][0]['id']
    
    # Obtener diagrama
    diagram_response = requests.get(f"{BASE_URL}/diagrams/?project={project_id}", headers=headers)
    if diagram_response.status_code != 200 or not diagram_response.json()['results']:
        # Crear un diagrama si no existe
        diagram_data = {
            "name": "Test Diagram for Versions",
            "project_id": project_id
        }
        create_response = requests.post(f"{BASE_URL}/diagrams/", json=diagram_data, headers=headers)
        if create_response.status_code != 201:
            raise Exception(f"Error creando diagrama: {create_response.text}")
        return create_response.json()['id']
    
    return diagram_response.json()['results'][0]['id']


def test_m04_create_diagram_version():
    """M04 - Crear versión del diagrama."""
    print("\n🔄 M04 - Crear versión del diagrama")
    print("-" * 50)
    
    headers = get_auth_headers()
    diagram_id = get_diagram_id()
    
    # Snapshot de ejemplo
    snapshot = {
        "classes": [
            {
                "id": str(uuid.uuid4()),
                "name": "User",
                "attributes": [
                    {"name": "id", "type": "UUID"},
                    {"name": "username", "type": "String"},
                    {"name": "email", "type": "String"}
                ],
                "methods": [
                    {"name": "authenticate", "returnType": "Boolean"}
                ]
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Profile",
                "attributes": [
                    {"name": "bio", "type": "Text"},
                    {"name": "avatar", "type": "String"}
                ]
            }
        ],
        "relations": [
            {
                "id": str(uuid.uuid4()),
                "type": "OneToOne",
                "from_class": "User",
                "to_class": "Profile"
            }
        ],
        "metadata": {
            "version": "1.0",
            "created_at": "2025-01-01T10:00:00Z",
            "tool": "DiagramEditor"
        }
    }
    
    # Crear versión
    version_data = {
        "diagram_id": diagram_id,
        "snapshot": snapshot,
        "message": "Versión inicial con User y Profile"
    }
    
    response = requests.post(f"{BASE_URL}/diagram-versions/", json=version_data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print("✅ Versión creada exitosamente")
        print(f"   ID: {result['id']}")
        print(f"   Número de versión: {result['version_number']}")
        print(f"   Mensaje: {result['message']}")
        print(f"   Creador: {result['created_by_username']}")
        return result['id']
    else:
        print(f"❌ Error: {response.text}")
        return None


def test_m04_create_second_version():
    """M04 - Crear segunda versión del diagrama."""
    print("\n🔄 M04 - Crear segunda versión del diagrama")
    print("-" * 50)
    
    headers = get_auth_headers()
    diagram_id = get_diagram_id()
    
    # Snapshot más complejo
    snapshot = {
        "classes": [
            {
                "id": str(uuid.uuid4()),
                "name": "User",
                "attributes": [
                    {"name": "id", "type": "UUID"},
                    {"name": "username", "type": "String"},
                    {"name": "email", "type": "String"},
                    {"name": "created_at", "type": "DateTime"}  # Nuevo campo
                ],
                "methods": [
                    {"name": "authenticate", "returnType": "Boolean"},
                    {"name": "update_profile", "returnType": "Boolean"}  # Nuevo método
                ]
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Profile",
                "attributes": [
                    {"name": "bio", "type": "Text"},
                    {"name": "avatar", "type": "String"},
                    {"name": "birth_date", "type": "Date"}  # Nuevo campo
                ]
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Address",  # Nueva clase
                "attributes": [
                    {"name": "street", "type": "String"},
                    {"name": "city", "type": "String"},
                    {"name": "country", "type": "String"}
                ]
            }
        ],
        "relations": [
            {
                "id": str(uuid.uuid4()),
                "type": "OneToOne",
                "from_class": "User",
                "to_class": "Profile"
            },
            {
                "id": str(uuid.uuid4()),
                "type": "OneToMany",
                "from_class": "User",
                "to_class": "Address"
            }
        ],
        "metadata": {
            "version": "1.1",
            "created_at": "2025-01-01T11:00:00Z",
            "tool": "DiagramEditor",
            "changes": ["Added Address class", "Added created_at to User", "Added birth_date to Profile"]
        }
    }
    
    version_data = {
        "diagram_id": diagram_id,
        "snapshot": snapshot,
        "message": "Agregada clase Address y nuevos campos"
    }
    
    response = requests.post(f"{BASE_URL}/diagram-versions/", json=version_data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print("✅ Segunda versión creada exitosamente")
        print(f"   ID: {result['id']}")
        print(f"   Número de versión: {result['version_number']}")
        print(f"   Mensaje: {result['message']}")
        return result['id']
    else:
        print(f"❌ Error: {response.text}")
        return None


def test_m05_list_diagram_versions():
    """M05 - Listar versiones de un diagrama."""
    print("\n📋 M05 - Listar versiones de un diagrama")
    print("-" * 50)
    
    headers = get_auth_headers()
    diagram_id = get_diagram_id()
    
    response = requests.get(f"{BASE_URL}/diagram-versions/?diagram={diagram_id}", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("✅ Versiones listadas exitosamente")
        print(f"   Total de versiones: {result['count']}")
        
        for version in result['results']:
            print(f"\n   📋 Versión {version['version_number']}:")
            print(f"      ID: {version['id']}")
            print(f"      Mensaje: {version['message']}")
            print(f"      Creador: {version['created_by_username']}")
            print(f"      Fecha: {version['created_at']}")
            print(f"      Tamaño snapshot: {version['snapshot_size']}")
        
        return result['results']
    else:
        print(f"❌ Error: {response.text}")
        return []


def test_m05_list_with_ordering():
    """M05 - Listar versiones con ordenamiento."""
    print("\n📋 M05 - Listar versiones con ordenamiento ascendente")
    print("-" * 50)
    
    headers = get_auth_headers()
    diagram_id = get_diagram_id()
    
    response = requests.get(
        f"{BASE_URL}/diagram-versions/?diagram={diagram_id}&ordering=version_number", 
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("✅ Versiones listadas con ordenamiento")
        
        version_numbers = [v['version_number'] for v in result['results']]
        print(f"   Números de versión: {version_numbers}")
        
        return result['results']
    else:
        print(f"❌ Error: {response.text}")
        return []


def test_m06_retrieve_diagram_version(version_id=None):
    """M06 - Obtener versión específica del diagrama."""
    print("\n🔍 M06 - Obtener versión específica del diagrama")
    print("-" * 50)
    
    headers = get_auth_headers()
    
    if not version_id:
        # Obtener la primera versión disponible
        versions = test_m05_list_diagram_versions()
        if not versions:
            print("❌ No hay versiones disponibles")
            return None
        version_id = versions[0]['id']
    
    response = requests.get(f"{BASE_URL}/diagram-versions/{version_id}/", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("✅ Versión obtenida exitosamente")
        print(f"   ID: {result['id']}")
        print(f"   Número de versión: {result['version_number']}")
        print(f"   Diagrama: {result['diagram_name']}")
        print(f"   Proyecto: {result['project_name']}")
        print(f"   Mensaje: {result['message']}")
        print(f"   Creador: {result['created_by_username']} ({result['created_by_email']})")
        print(f"   Fecha: {result['created_at']}")
        
        # Mostrar información del snapshot
        snapshot = result['snapshot']
        classes_count = len(snapshot.get('classes', []))
        relations_count = len(snapshot.get('relations', []))
        
        print(f"\n   📊 Contenido del snapshot:")
        print(f"      Clases: {classes_count}")
        print(f"      Relaciones: {relations_count}")
        
        if classes_count > 0:
            print(f"      Clases incluidas:")
            for cls in snapshot['classes']:
                attr_count = len(cls.get('attributes', []))
                method_count = len(cls.get('methods', []))
                print(f"        - {cls['name']}: {attr_count} atributos, {method_count} métodos")
        
        return result
    else:
        print(f"❌ Error: {response.text}")
        return None


def test_error_cases():
    """Pruebas de casos de error."""
    print("\n⚠️  Pruebas de casos de error")
    print("-" * 50)
    
    headers = get_auth_headers()
    
    # M04 - Crear versión con diagram_id inválido
    print("\n1. M04 - Crear versión con diagram_id inválido")
    invalid_data = {
        "diagram_id": str(uuid.uuid4()),
        "snapshot": {"classes": [], "relations": [], "metadata": {}},
        "message": "Test"
    }
    response = requests.post(f"{BASE_URL}/diagram-versions/", json=invalid_data, headers=headers)
    print(f"   Status: {response.status_code} (esperado: 400)")
    if response.status_code == 400:
        print("   ✅ Error manejado correctamente")
    
    # M04 - Crear versión con snapshot inválido
    print("\n2. M04 - Crear versión con snapshot inválido")
    diagram_id = get_diagram_id()
    invalid_snapshot = {
        "diagram_id": diagram_id,
        "snapshot": {"invalid": "structure"},  # Estructura inválida
        "message": "Test"
    }
    response = requests.post(f"{BASE_URL}/diagram-versions/", json=invalid_snapshot, headers=headers)
    print(f"   Status: {response.status_code} (esperado: 400)")
    if response.status_code == 400:
        print("   ✅ Error manejado correctamente")
    
    # M05 - Listar sin parámetro diagram
    print("\n3. M05 - Listar sin parámetro diagram")
    response = requests.get(f"{BASE_URL}/diagram-versions/", headers=headers)
    print(f"   Status: {response.status_code} (esperado: 400)")
    if response.status_code == 400:
        print("   ✅ Error manejado correctamente")
    
    # M06 - Obtener versión inexistente
    print("\n4. M06 - Obtener versión inexistente")
    fake_id = str(uuid.uuid4())
    response = requests.get(f"{BASE_URL}/diagram-versions/{fake_id}/", headers=headers)
    print(f"   Status: {response.status_code} (esperado: 404)")
    if response.status_code == 404:
        print("   ✅ Error manejado correctamente")


if __name__ == "__main__":
    print("🚀 Testing Diagram Versions Endpoints (M04, M05, M06)")
    print("=" * 60)
    
    try:
        # Crear versiones
        version1_id = test_m04_create_diagram_version()
        version2_id = test_m04_create_second_version()
        
        # Listar versiones
        versions = test_m05_list_diagram_versions()
        test_m05_list_with_ordering()
        
        # Obtener versión específica
        if versions:
            test_m06_retrieve_diagram_version(versions[0]['id'])
        
        # Casos de error
        test_error_cases()
        
        print("\n" + "=" * 60)
        print("✅ Pruebas de versiones de diagramas completadas")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()