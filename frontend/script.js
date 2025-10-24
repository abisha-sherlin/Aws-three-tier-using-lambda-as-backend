// Replace with your backend API Gateway endpoint or ELB URL
const backendUrl = "https://y4now77067.execute-api.us-east-1.amazonaws.com/api/items";

// Select DOM elements
const itemsList = document.getElementById("itemsList");
const addBtn = document.getElementById("addBtn");
const fetchBtn = document.getElementById("fetchBtn");
const itemInput = document.getElementById("itemName");

// Fetch items from backend
async function fetchItems() {
  itemsList.innerHTML = "<li>Loading...</li>";

  try {
    const response = await fetch(backendUrl, {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) throw new Error(`Error: ${response.statusText}`);

    const data = await response.json();
    itemsList.innerHTML = "";

    if (!data.length) {
      itemsList.innerHTML = "<li>No items found</li>";
      return;
    }

    data.forEach(item => {
      const li = document.createElement("li");
      li.textContent = `${item.id}: ${item.name}`;
      itemsList.appendChild(li);
    });

  } catch (err) {
    console.error(err);
    itemsList.innerHTML = "<li>Error loading items.</li>";
  }
}

// Add new item to backend
async function addItem() {
  const name = itemInput.value.trim();
  if (!name) return alert("Please enter an item name.");

  try {
    const response = await fetch(backendUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ name })
    });

    if (!response.ok) throw new Error(`Error: ${response.statusText}`);

    itemInput.value = "";
    fetchItems(); // refresh list

  } catch (err) {
    console.error(err);
    alert("Error adding item.");
  }
}

// Event listeners
addBtn.addEventListener("click", addItem);
fetchBtn.addEventListener("click", fetchItems);

// Optional: fetch items on page load
window.addEventListener("DOMContentLoaded", fetchItems);
