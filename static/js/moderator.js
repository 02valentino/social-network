function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function toggleBanUser(button) {
  const userId = button.getAttribute("data-user-id");
  const isBanned = button.getAttribute("data-is-banned") === "true";
  const csrfToken = getCookie("csrftoken");

  if (!csrfToken) {
    alert("Authentication error. Please refresh the page.");
    return;
  }

  button.disabled = true;
  const originalText = button.textContent;
  button.textContent = "Processing...";

  fetch(`/moderator/toggle-ban/${userId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
      "X-Requested-With": "XMLHttpRequest",
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        return response.json().then((data) => {
          throw new Error(data.error || "Network error");
        });
      }
      return response.json();
    })
    .then((data) => {
      if (data.success) {
        button.textContent = data.button_text;
        button.setAttribute("data-is-banned", data.is_banned.toString());

        if (data.is_banned) {
          button.classList.remove("ban-btn");
          button.classList.add("unban-btn");
        } else {
          button.classList.remove("unban-btn");
          button.classList.add("ban-btn");
        }

        const statusElement = document.getElementById(`status-${userId}`);
        if (statusElement) {
          statusElement.textContent = data.is_banned ? "Banned" : "Active";
          statusElement.className = `user-status ${
            data.is_banned ? "banned" : "active"
          }`;
        }
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      button.textContent = originalText;
    })
    .finally(() => {
      button.disabled = false;
    });
}

function deletePost(button) {
  const postId = button.getAttribute("data-post-id");
  const csrfToken = getCookie("csrftoken");

  if (!csrfToken) {
    alert("Authentication error. Please refresh the page.");
    return;
  }

  button.disabled = true;
  const originalText = button.textContent;
  button.textContent = "Deleting...";

  fetch(`/moderator/delete-post/${postId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
      "X-Requested-With": "XMLHttpRequest",
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        return response.json().then((data) => {
          throw new Error(data.error || "Network error");
        });
      }
      return response.json();
    })
    .then((data) => {
      if (data.success) {
        const postItem = document.getElementById(`post-item-${postId}`);
        if (postItem) {
          postItem.style.transition = "opacity 0.3s ease-out";
          postItem.style.opacity = "0";
          setTimeout(() => {
            postItem.remove();

            const postsList = document.querySelector(".mod-posts-list");
            if (postsList && postsList.children.length === 0) {
              const container = document.querySelector(".mod-posts-container");
              if (container) {
                container.innerHTML =
                  '<div class="mod-empty-state">No posts found from regular users.</div>';
              }
            }
          }, 300);
        }
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      button.textContent = originalText;
      button.disabled = false;
    });
}

window.toggleBanUser = toggleBanUser;
window.deletePost = deletePost;
