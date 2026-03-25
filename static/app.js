// Load items from GET /api/items and render table
async function loadItems() {
    try {
        const response = await fetch('/api/items');
        if (!response.ok) {
            throw new Error('Failed to load items');
        }
        const items = await response.json();
        renderTable(items);
    } catch (error) {
        console.error('Error loading items:', error);
        alert('Error loading items: ' + error.message);
    }
}

// Render items table
function renderTable(items) {
    const tbody = document.getElementById('itemsBody');
    tbody.innerHTML = '';
    
    if (items.length === 0) {
        const row = tbody.insertRow();
        const cell = row.insertCell(0);
        cell.colSpan = 4;
        cell.textContent = 'No items found';
        return;
    }
    
    items.forEach(item => {
        const row = tbody.insertRow();
        row.insertCell(0).textContent = item.item_id;
        row.insertCell(1).textContent = item.name;
        row.insertCell(2).textContent = '$' + item.price.toFixed(2);
        row.insertCell(3).textContent = item.in_stock ? 'Yes' : 'No';
    });
}

// Save item using POST /api/items/{item_id}
async function saveItem() {
    const item_id = parseInt(document.getElementById('item_id').value);
    const name = document.getElementById('name').value;
    const price = parseFloat(document.getElementById('price').value);
    const in_stock = document.getElementById('in_stock').checked;
    
    if (isNaN(item_id) || !name || isNaN(price)) {
        alert('Please fill in all required fields');
        return;
    }
    
    const item = {
        name: name,
        price: price,
        in_stock: in_stock
    };
    
    try {
        const response = await fetch('/api/items/' + item_id, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(item)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to save item');
        }
        
        // Reload items after save
        loadItems();
    } catch (error) {
        console.error('Error saving item:', error);
        alert('Error saving item: ' + error.message);
    }
}

// Delete item using DELETE /api/items/{item_id}
async function deleteItem() {
    const item_id = parseInt(document.getElementById('item_id').value);
    
    if (isNaN(item_id)) {
        alert('Please enter a valid item ID');
        return;
    }
    
    try {
        const response = await fetch('/api/items/' + item_id, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to delete item');
        }
        
        // Reload items after delete
        loadItems();
    } catch (error) {
        console.error('Error deleting item:', error);
        alert('Error deleting item: ' + error.message);
    }
}
