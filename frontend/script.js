const backendUrl = "http://backend-app-lb-2127459385.us-east-1.elb.amazonaws.com/api/items"; // Replace with your backend endpoint

// Fetch items from backend
async function fetchItems() {
  const list = document.getElementById("itemsList");
  list.innerHTML = "Loading...";

  try {
    const response = await fetch(backendUrl);
    if (!response.ok) throw new Error("Failed to fetch items");

    const data = await response.json();
    list.innerHTML = "";

    if (data.length === 0) {
      list.innerHTML = "<li>No items found</li>";
      return;
    }

    data.forEach(item => {
      const li = document.createElement("li");
      li.textContent = `${item.id}: ${item.name}`;
      list.appendChild(li);
    });
  } catch (err) {
    console.error(err);
    list.innerHTML = "<li>Error loading items.</li>";
  }
}

// Add new item to backend
async function addItem() {
  const itemName = document.getElementById("itemName").value.trim();
  if (!itemName) {
    alert("Please enter an item name.");
    return;
  }

  try {
    const response = await fetch(backendUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ name: itemName })
    });

    if (!response.ok) throw new Error("Failed to add item");

    document.getElementById("itemName").value = "";
    fetchItems(); // refresh the list
  } catch (err) {
    console.error(err);
    alert("Error adding item.");
  }
}
