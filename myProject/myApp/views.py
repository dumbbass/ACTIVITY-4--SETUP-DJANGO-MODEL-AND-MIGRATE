from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item
import json

# Create your views here.

# Root endpoint that lists all available API endpoints
def api_root(request):
    data = {
        'message': 'Welcome to the Items API',
        'available_endpoints': {
            'Basic API Endpoints': {
                'GET /api/hello/': 'Basic hello world API endpoint',
                'GET /api/greet/?name=YourName': 'Greeting endpoint with query parameter',
                'POST /api/submit/': 'Submit endpoint for handling POST requests',
                'GET/POST /api/combined/': 'Combined endpoint handling both GET and POST',
            },
            'Item API Endpoints': {
                'GET /api/items/': 'List all items or filter with ?search=query',
                'POST /api/items/add/': 'Add a new item',
                'GET /api/items/<item_id>/': 'Get a single item by ID',
                'PUT /api/items/update/<item_id>/': 'Update an item by ID',
                'DELETE /api/items/delete/<item_id>/': 'Delete an item by ID',
            }
        },
        'status': 'success'
    }
    return JsonResponse(data)

# Basic API endpoint
def hello_api(request):
    data = {
        'message': 'Hello, API World!',
        'status': 'success'
    }
    return JsonResponse(data)

# API endpoint that handles GET with query parameters
def greet_api(request):
    name = request.GET.get('name', 'Guest')
    data = {
        'message': f'Hello, {name}!',
        'status': 'success',
        'method': 'GET'
    }
    return JsonResponse(data)

# API endpoint for handling POST requests
@csrf_exempt  # Disable CSRF for simplicity in this example
def submit_api(request):
    if request.method == 'POST':
        try:
            # Handle form data
            if request.content_type == 'application/x-www-form-urlencoded':
                name = request.POST.get('name', 'Guest')
                email = request.POST.get('email', 'No email provided')
                
                data = {
                    'message': 'Form data received successfully!',
                    'name': name,
                    'email': email,
                    'status': 'success',
                    'method': 'POST'
                }
                
            # Handle JSON data
            elif request.content_type == 'application/json':
                body_data = json.loads(request.body.decode('utf-8'))
                name = body_data.get('name', 'Guest')
                email = body_data.get('email', 'No email provided')
                
                data = {
                    'message': 'JSON data received successfully!',
                    'name': name,
                    'email': email,
                    'status': 'success',
                    'method': 'POST'
                }
                
            else:
                data = {
                    'message': 'Unsupported content type',
                    'status': 'error',
                    'method': 'POST'
                }
                
        except Exception as e:
            data = {
                'message': f'Error processing request: {str(e)}',
                'status': 'error',
                'method': 'POST'
            }
            
    else:
        data = {
            'message': 'This endpoint only accepts POST requests',
            'status': 'error',
            'method': request.method
        }
        
    return JsonResponse(data)

# API endpoint handling both GET and POST
@csrf_exempt
def combined_api(request):
    if request.method == 'GET':
        # Handle GET request with query parameters
        action = request.GET.get('action', 'default')
        value = request.GET.get('value', '')
        
        data = {
            'message': f'GET request received with action: {action}',
            'value': value,
            'status': 'success',
            'method': 'GET'
        }
        
    elif request.method == 'POST':
        # Handle POST request
        try:
            if request.content_type == 'application/x-www-form-urlencoded':
                action = request.POST.get('action', 'default')
                value = request.POST.get('value', '')
            elif request.content_type == 'application/json':
                body_data = json.loads(request.body.decode('utf-8'))
                action = body_data.get('action', 'default')
                value = body_data.get('value', '')
            else:
                action = 'unknown'
                value = 'unknown'
                
            data = {
                'message': f'POST request received with action: {action}',
                'value': value,
                'status': 'success',
                'method': 'POST'
            }
            
        except Exception as e:
            data = {
                'message': f'Error processing request: {str(e)}',
                'status': 'error',
                'method': 'POST'
            }
    else:
        data = {
            'message': f'Method {request.method} not supported',
            'status': 'error',
            'method': request.method
        }
        
    return JsonResponse(data)

# Item API Endpoints

def items_list(request):
    """
    a. GET /api/items/ → Return all items.
    b. GET /api/items/?search=Item → Filter items using a query parameter.
    """
    search_query = request.GET.get('search', '')
    
    if search_query:
        # Filter items by name containing the search query
        items = Item.objects.filter(name__icontains=search_query)
    else:
        # Get all items
        items = Item.objects.all()
    
    # Convert queryset to list of dictionaries
    items_data = []
    for item in items:
        items_data.append({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': str(item.price),
            'created_at': item.created_at.isoformat(),
            'updated_at': item.updated_at.isoformat()
        })
    
    return JsonResponse({
        'items': items_data,
        'count': len(items_data),
        'status': 'success'
    })

@csrf_exempt
def add_item(request):
    """
    c. POST /api/items/add/ → Add a new item (JSON or form data).
    """
    if request.method != 'POST':
        return JsonResponse({
            'message': 'This endpoint only accepts POST requests',
            'status': 'error'
        }, status=405)
    
    try:
        # Process data based on content type
        if request.content_type == 'application/x-www-form-urlencoded':
            # Handle form data
            name = request.POST.get('name')
            description = request.POST.get('description', '')
            price = request.POST.get('price')
            
        elif request.content_type == 'application/json':
            # Handle JSON data
            body_data = json.loads(request.body.decode('utf-8'))
            name = body_data.get('name')
            description = body_data.get('description', '')
            price = body_data.get('price')
            
        else:
            return JsonResponse({
                'message': 'Unsupported content type',
                'status': 'error'
            }, status=415)
        
        # Validate required fields
        if not name or not price:
            return JsonResponse({
                'message': 'Name and price are required fields',
                'status': 'error'
            }, status=400)
        
        # Create new item
        item = Item.objects.create(
            name=name,
            description=description,
            price=price
        )
        
        # Return success response with item data
        return JsonResponse({
            'message': 'Item created successfully',
            'status': 'success',
            'item': {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'price': str(item.price),
                'created_at': item.created_at.isoformat(),
                'updated_at': item.updated_at.isoformat()
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'message': 'Invalid JSON data',
            'status': 'error'
        }, status=400)
        
    except Exception as e:
        return JsonResponse({
            'message': f'Error creating item: {str(e)}',
            'status': 'error'
        }, status=500)

def item_detail(request, item_id):
    """
    d. GET /api/items/<int:item_id>/ → Get a single item.
    """
    try:
        # Get item by ID or return 404
        item = get_object_or_404(Item, id=item_id)
        
        # Return item data
        return JsonResponse({
            'status': 'success',
            'item': {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'price': str(item.price),
                'created_at': item.created_at.isoformat(),
                'updated_at': item.updated_at.isoformat()
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'message': f'Error retrieving item: {str(e)}',
            'status': 'error'
        }, status=500)

@csrf_exempt
def update_item(request, item_id):
    """
    e. PUT /api/items/update/<int:item_id>/ → Update an item (JSON or form data).
    """
    if request.method not in ['PUT', 'POST']:
        return JsonResponse({
            'message': 'This endpoint only accepts PUT or POST requests',
            'status': 'error'
        }, status=405)
    
    try:
        # Get item by ID or return 404
        item = get_object_or_404(Item, id=item_id)
        
        # Process data based on content type
        if request.content_type == 'application/x-www-form-urlencoded':
            # Handle form data
            name = request.POST.get('name', item.name)
            description = request.POST.get('description', item.description)
            price = request.POST.get('price', item.price)
            
        elif request.content_type == 'application/json':
            # Handle JSON data
            body_data = json.loads(request.body.decode('utf-8'))
            name = body_data.get('name', item.name)
            description = body_data.get('description', item.description)
            price = body_data.get('price', str(item.price))
            
        else:
            return JsonResponse({
                'message': 'Unsupported content type',
                'status': 'error'
            }, status=415)
        
        # Update item
        item.name = name
        item.description = description
        if price is not None:
            item.price = price
        item.save()
        
        # Return success response with updated item data
        return JsonResponse({
            'message': 'Item updated successfully',
            'status': 'success',
            'item': {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'price': str(item.price),
                'created_at': item.created_at.isoformat(),
                'updated_at': item.updated_at.isoformat()
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'message': 'Invalid JSON data',
            'status': 'error'
        }, status=400)
        
    except Exception as e:
        return JsonResponse({
            'message': f'Error updating item: {str(e)}',
            'status': 'error'
        }, status=500)

@csrf_exempt
def delete_item(request, item_id):
    """
    f. DELETE /api/items/delete/<int:item_id>/ → Delete an item.
    """
    if request.method != 'DELETE':
        return JsonResponse({
            'message': 'This endpoint only accepts DELETE requests',
            'status': 'error'
        }, status=405)
    
    try:
        # Get item by ID or return 404
        item = get_object_or_404(Item, id=item_id)
        
        # Store item name for response
        item_name = item.name
        
        # Delete the item
        item.delete()
        
        # Return success response
        return JsonResponse({
            'message': f'Item "{item_name}" deleted successfully',
            'status': 'success',
            'item_id': item_id
        })
        
    except Exception as e:
        return JsonResponse({
            'message': f'Error deleting item: {str(e)}',
            'status': 'error'
        }, status=500)
