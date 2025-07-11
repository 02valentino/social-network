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

function handleLikeClick(button) {
  try {
    var postId = button.getAttribute("data-post-id");
    var csrfTokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
    var csrfToken =
      (csrfTokenElement && csrfTokenElement.value) || getCookie("csrftoken");

    if (!csrfToken) {
      alert("Please log in to like posts.");
      return false;
    }

    button.disabled = true;

    fetch("/post/" + postId + "/like/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("Network error: " + response.status);
        }
        return response.json();
      })
      .then(function (data) {
        var likeIcon = document.querySelector(
          "#like-container-" + postId + " .like-icon"
        );
        var likeCount = document.querySelector(
          "#like-container-" + postId + " .like-count"
        );

        if (likeIcon) {
          likeIcon.textContent = data.like_icon;

          likeIcon.style.transform = "scale(1.2)";
          setTimeout(function () {
            likeIcon.style.transform = "scale(1)";
          }, 150);
        }

        if (likeCount) {
          if (data.like_count > 0) {
            likeCount.innerHTML =
              '<a href="/post/' +
              postId +
              '/likes/" class="text-decoration-none text-muted" title="View who liked this post">' +
              data.like_count +
              "</a>";
          } else {
            likeCount.innerHTML = '<span class="text-muted">0</span>';
          }
        }
      })
      .catch(function (error) {
        console.error("Like error:", error);
        alert("Unable to like post. Please try again.");
      })
      .finally(function () {
        button.disabled = false;
      });
  } catch (error) {
    console.error("JavaScript error:", error);
    alert("An error occurred. Please try again.");
  }

  return false;
}

document.addEventListener("DOMContentLoaded", function () {
  initializeCommentEventListeners();
});

function initializeCommentEventListeners() {
  var commentForms = document.querySelectorAll(".comment-form");
  commentForms.forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var postId = form.getAttribute("data-post-id") || getPostIdFromUrl();
      submitComment(form, postId);
    });
  });

  document.addEventListener("click", function (e) {
    var target = e.target;

    if (target.matches('[data-action="edit-comment"]')) {
      e.preventDefault();
      var commentId = target.getAttribute("data-comment-id");
      startEditComment(commentId);
    }

    if (target.matches('[data-action="delete-comment"]')) {
      e.preventDefault();
      var commentId = target.getAttribute("data-comment-id");
      var postId = target.getAttribute("data-post-id");
      deleteComment(commentId, postId);
    }
  });
}

function getPostIdFromUrl() {
  var pathParts = window.location.pathname.split("/");
  for (var i = 0; i < pathParts.length; i++) {
    if (pathParts[i] === "post" && pathParts[i + 1]) {
      return pathParts[i + 1];
    }
  }
  return null;
}

function submitComment(form, postId) {
  try {
    var formData = new FormData(form);
    var csrfToken =
      formData.get("csrfmiddlewaretoken") || getCookie("csrftoken");

    if (!csrfToken) {
      alert("Please log in to comment.");
      return false;
    }

    var submitBtn = form.querySelector('button[type="submit"]');
    var originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML =
      '<i class="fas fa-spinner fa-spin me-1"></i>Posting...';

    fetch("/post/" + postId + "/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "X-Requested-With": "XMLHttpRequest",
      },
      body: formData,
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("Network error: " + response.status);
        }
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          form.reset();

          addCommentToList(data.comment, postId);

          updateCommentCount(postId, data.comment_count);
        } else {
          throw new Error(data.error || "Failed to post comment");
        }
      })
      .catch(function (error) {
        console.error("Comment error:", error);
        showMessage("Unable to post comment: " + error.message, "error");
      })
      .finally(function () {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      });
  } catch (error) {
    console.error("JavaScript error:", error);
    showMessage("An error occurred. Please try again.", "error");
  }

  return false;
}

function editComment(commentId, newContent) {
  try {
    var csrfToken = getCookie("csrftoken");

    if (!csrfToken) {
      alert("Please log in to edit comments.");
      return false;
    }

    fetch("/comment/" + commentId + "/edit/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
        "X-Requested-With": "XMLHttpRequest",
      },
      body: JSON.stringify({ content: newContent }),
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("Network error: " + response.status);
        }
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          var commentElement = document.querySelector(
            '[data-comment-id="' + commentId + '"] .comment-content'
          );
          if (commentElement) {
            commentElement.textContent = newContent;
          }
        } else {
          throw new Error(data.error || "Failed to update comment");
        }
      })
      .catch(function (error) {
        console.error("Edit comment error:", error);
        showMessage("Unable to update comment: " + error.message, "error");
      });
  } catch (error) {
    console.error("JavaScript error:", error);
    showMessage("An error occurred. Please try again.", "error");
  }
}

function deleteComment(commentId, postId) {
  try {
    var csrfToken = getCookie("csrftoken");

    if (!csrfToken) {
      alert("Please log in to delete comments.");
      return false;
    }

    fetch("/comment/" + commentId + "/delete/", {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("Network error: " + response.status);
        }
        return response.text();
      })
      .then(function (html) {
        showDeleteConfirmationModal(html, commentId, postId);
      })
      .catch(function (error) {
        console.error("Delete comment error:", error);
        showMessage(
          "Unable to load delete confirmation: " + error.message,
          "error"
        );
      });
  } catch (error) {
    console.error("JavaScript error:", error);
    showMessage("An error occurred. Please try again.", "error");
  }
}

function showDeleteConfirmationModal(htmlContent, commentId, postId) {
  var modalHtml = `
    <div class="modal fade" id="deleteCommentModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title">
              <i class="fas fa-exclamation-triangle me-2"></i>Confirm Comment Deletion
            </h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div id="modal-content-placeholder"></div>
          </div>
        </div>
      </div>
    </div>
  `;

  var existingModal = document.getElementById("deleteCommentModal");
  if (existingModal) {
    existingModal.remove();
  }

  document.body.insertAdjacentHTML("beforeend", modalHtml);

  var parser = new DOMParser();
  var doc = parser.parseFromString(htmlContent, "text/html");
  var cardBody = doc.querySelector(".card-body");

  if (cardBody) {
    var modalContent = document.getElementById("modal-content-placeholder");
    modalContent.innerHTML = cardBody.innerHTML;

    var form = modalContent.querySelector("form");
    if (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        confirmDeleteComment(commentId, postId);
      });

      var cancelBtn = modalContent.querySelector(".btn-secondary");
      if (cancelBtn) {
        cancelBtn.addEventListener("click", function (e) {
          e.preventDefault();
          var modal = bootstrap.Modal.getInstance(
            document.getElementById("deleteCommentModal")
          );
          modal.hide();
        });
      }
    }
  }

  var modal = new bootstrap.Modal(
    document.getElementById("deleteCommentModal")
  );
  modal.show();

  document
    .getElementById("deleteCommentModal")
    .addEventListener("hidden.bs.modal", function () {
      this.remove();
    });
}

function confirmDeleteComment(commentId, postId) {
  try {
    var csrfToken = getCookie("csrftoken");

    if (!csrfToken) {
      alert("Please log in to delete comments.");
      return false;
    }

    var deleteBtn = document.querySelector("#deleteCommentModal .btn-danger");
    var originalText = deleteBtn.innerHTML;
    deleteBtn.disabled = true;
    deleteBtn.innerHTML =
      '<i class="fas fa-spinner fa-spin me-1"></i>Deleting...';

    fetch("/comment/" + commentId + "/delete/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("Network error: " + response.status);
        }
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          var modal = bootstrap.Modal.getInstance(
            document.getElementById("deleteCommentModal")
          );
          modal.hide();

          var commentElement = document.querySelector(
            '[data-comment-id="' + commentId + '"]'
          );
          if (commentElement) {
            commentElement.remove();
          }

          updateCommentCount(postId, data.comment_count);
        } else {
          throw new Error(data.error || "Failed to delete comment");
        }
      })
      .catch(function (error) {
        console.error("Delete comment error:", error);
        showMessage("Unable to delete comment: " + error.message, "error");
      })
      .finally(function () {
        deleteBtn.disabled = false;
        deleteBtn.innerHTML = originalText;
      });
  } catch (error) {
    console.error("JavaScript error:", error);
    showMessage("An error occurred. Please try again.", "error");
  }
}

function addCommentToList(comment, postId) {
  var commentsList = document.querySelector(".comments-list");
  if (!commentsList) return;

  var noCommentsMsg = commentsList.querySelector(".no-comments");
  if (noCommentsMsg) {
    noCommentsMsg.remove();
  }

  var commentHtml = `
    <li class="list-group-item" data-comment-id="${comment.id}">
      <div class="d-flex justify-content-between align-items-start">
        <div class="d-flex align-items-start flex-grow-1">
          <div class="me-3 flex-shrink-0">
            ${
              comment.author_avatar
                ? `<img src="${comment.author_avatar}" class="rounded-circle post-avatar" width="32" height="32" alt="User Picture" />`
                : `<div class="rounded-circle avatar-placeholder avatar-sm"><i class="fas fa-user"></i></div>`
            }
          </div>
          <div class="flex-grow-1">
            <div class="mb-1">
              <strong>${comment.author}</strong>
              <small class="text-muted ms-2">${comment.created_at}</small>
            </div>
            <p class="mb-0 comment-content">${comment.content}</p>
          </div>
        </div>
        ${
          comment.can_edit
            ? `
        <div class="dropdown">
          <button class="btn btn-sm btn-light dropdown-toggle" type="button" data-bs-toggle="dropdown">⋮</button>
          <ul class="dropdown-menu dropdown-menu-end">
            <li><a class="dropdown-item" href="#" data-action="edit-comment" data-comment-id="${comment.id}">Edit</a></li>
            <li><a class="dropdown-item text-danger" href="#" data-action="delete-comment" data-comment-id="${comment.id}" data-post-id="${postId}">Delete</a></li>
          </ul>
        </div>
        `
            : ""
        }
      </div>
    </li>
  `;

  commentsList.insertAdjacentHTML("beforeend", commentHtml);
}

function updateCommentCount(postId, count) {
  var commentCountElements = document.querySelectorAll(
    '[data-post-id="' + postId + '"] .comment-count'
  );
  commentCountElements.forEach(function (element) {
    element.textContent = count;
  });
}

function startEditComment(commentId) {
  var commentElement = document.querySelector(
    '[data-comment-id="' + commentId + '"] .comment-content'
  );
  if (!commentElement) return;

  var currentContent = commentElement.textContent;
  var editHtml = `
    <div class="edit-comment-form">
      <textarea class="form-control mb-2" rows="3">${currentContent}</textarea>
      <div>
        <button class="btn btn-sm btn-primary me-2" data-action="save-edit" data-comment-id="${commentId}">Save</button>
        <button class="btn btn-sm btn-secondary" data-action="cancel-edit" data-comment-id="${commentId}" data-original-content="${currentContent}">Cancel</button>
      </div>
    </div>
  `;

  commentElement.innerHTML = editHtml;

  var saveBtn = commentElement.querySelector('[data-action="save-edit"]');
  var cancelBtn = commentElement.querySelector('[data-action="cancel-edit"]');

  saveBtn.addEventListener("click", function () {
    saveEditComment(commentId);
  });

  cancelBtn.addEventListener("click", function () {
    cancelEditComment(commentId, currentContent);
  });
}

function saveEditComment(commentId) {
  var commentElement = document.querySelector(
    '[data-comment-id="' + commentId + '"] .comment-content'
  );
  var textarea = commentElement.querySelector("textarea");
  if (!textarea) return;

  var newContent = textarea.value.trim();
  if (!newContent) {
    alert("Comment cannot be empty.");
    return false;
  }

  editComment(commentId, newContent);
}

function cancelEditComment(commentId, originalContent) {
  var commentElement = document.querySelector(
    '[data-comment-id="' + commentId + '"] .comment-content'
  );
  if (commentElement) {
    commentElement.textContent = originalContent;
  }
}

function showMessage(message, type) {
  var alertClass = type === "success" ? "alert-success" : "alert-danger";
  var messageHtml = `
    <div class="alert ${alertClass} alert-dismissible fade show position-fixed" style="top: 20px; right: 20px; z-index: 1050;">
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
  `;

  document.body.insertAdjacentHTML("beforeend", messageHtml);

  setTimeout(function () {
    var alert = document.querySelector(".alert:last-of-type");
    if (alert) {
      alert.remove();
    }
  }, 3000);
}

function deletePost(postId) {
  try {
    var csrfToken = getCookie("csrftoken");

    if (!csrfToken) {
      alert("Please log in to delete posts.");
      return false;
    }

    fetch("/post/" + postId + "/delete/", {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("Network error: " + response.status);
        }
        return response.text();
      })
      .then(function (html) {
        showPostDeleteConfirmationModal(html, postId);
      })
      .catch(function (error) {
        console.error("Delete post error:", error);
        showMessage(
          "Unable to load delete confirmation: " + error.message,
          "error"
        );
      });
  } catch (error) {
    console.error("JavaScript error:", error);
    showMessage("An error occurred. Please try again.", "error");
  }
}

function showPostDeleteConfirmationModal(htmlContent, postId) {
  var modalHtml = `
    <div class="modal fade" id="deletePostModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title">
              <i class="fas fa-exclamation-triangle me-2"></i>Confirm Post Deletion
            </h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div id="modal-post-content-placeholder"></div>
          </div>
        </div>
      </div>
    </div>
  `;

  c
  if (existingModal) {
    existingModal.remove();
  }

  document.body.insertAdjacentHTML("beforeend", modalHtml);

  var parser = new DOMParser();
  var doc = parser.parseFromString(htmlContent, "text/html");
  var cardBody = doc.querySelector(".card-body");

  if (cardBody) {
    var modalContent = document.getElementById(
      "modal-post-content-placeholder"
    );
    modalContent.innerHTML = cardBody.innerHTML;

    var form = modalContent.querySelector("form");
    if (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        confirmDeletePost(postId);
      });

      var cancelBtn = modalContent.querySelector(
        ".btn-outline-secondary, .btn-secondary, a[href*='history.back']"
      );
      if (cancelBtn) {
        cancelBtn.addEventListener("click", function (e) {
          e.preventDefault();
          var modal = bootstrap.Modal.getInstance(
            document.getElementById("deletePostModal")
          );
          modal.hide();
        });

        if (cancelBtn.href && cancelBtn.href.includes("history.back")) {
          cancelBtn.href = "#";
        }
      }
    }
  }

  var modal = new bootstrap.Modal(document.getElementById("deletePostModal"));
  modal.show();

  document
    .getElementById("deletePostModal")
    .addEventListener("hidden.bs.modal", function () {
      this.remove();
    });
}

function confirmDeletePost(postId) {
  try {
    var csrfToken = getCookie("csrftoken");

    if (!csrfToken) {
      alert("Please log in to delete posts.");
      return false;
    }

    var deleteBtn = document.querySelector("#deletePostModal .btn-danger");
    var originalText = deleteBtn.innerHTML;
    deleteBtn.disabled = true;
    deleteBtn.innerHTML =
      '<i class="fas fa-spinner fa-spin me-1"></i>Deleting...';

    fetch("/post/" + postId + "/delete/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("Network error: " + response.status);
        }
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          var modal = bootstrap.Modal.getInstance(
            document.getElementById("deletePostModal")
          );
          modal.hide();

          if (window.location.pathname.includes("/post/")) {
            window.location.href = data.redirect_url || "/posts/";
          } else {
            var postCard = document.querySelector(
              '[data-post-id="' + postId + '"]'
            );
            if (postCard) {
              postCard.remove();
            }
          }
        } else {
          throw new Error(data.error || "Failed to delete post");
        }
      })
      .catch(function (error) {
        console.error("Delete post error:", error);
        showMessage("Unable to delete post: " + error.message, "error");
      })
      .finally(function () {
        deleteBtn.disabled = false;
        deleteBtn.innerHTML = originalText;
      });
  } catch (error) {
    console.error("JavaScript error:", error);
    showMessage("An error occurred. Please try again.", "error");
  }
}

function editPost(postId) {
  try {
    var csrfToken = getCookie("csrftoken");

    if (!csrfToken) {
      alert("Please log in to edit posts.");
      return false;
    }

    fetch("/post/" + postId + "/edit/", {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("Network error: " + response.status);
        }
        return response.json();
      })
      .then(function (data) {
        showPostEditModal(data, postId);
      })
      .catch(function (error) {
        console.error("Edit post error:", error);
        alert("Unable to load edit form: " + error.message);
      });
  } catch (error) {
    console.error("JavaScript error:", error);
    alert("An error occurred. Please try again.");
  }

  return false;
}

function showPostEditModal(data, postId) {
  var modalHtml = `
    <div class="modal fade" id="editPostModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Post</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form id="editPostForm">
              ${data.form_html}
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-primary" onclick="savePostEdit(${postId})">Save Changes</button>
          </div>
        </div>
      </div>
    </div>
  `;

  var existingModal = document.getElementById("editPostModal");
  if (existingModal) {
    existingModal.remove();
  }

  document.body.insertAdjacentHTML("beforeend", modalHtml);

  var modal = new bootstrap.Modal(document.getElementById("editPostModal"));
  modal.show();

  document
    .getElementById("editPostModal")
    .addEventListener("hidden.bs.modal", function () {
      this.remove();
    });
}

function savePostEdit(postId) {
  try {
    var form = document.getElementById("editPostForm");
    var formData = new FormData();

    var contentField = form.querySelector('[name="content"]');
    var visibilityField = form.querySelector('[name="visibility"]');

    if (contentField) formData.append("content", contentField.value);
    if (visibilityField) formData.append("visibility", visibilityField.value);

    var csrfToken = getCookie("csrftoken");
    formData.append("csrfmiddlewaretoken", csrfToken);

    var saveBtn = document.querySelector("#editPostModal .btn-primary");
    var originalText = saveBtn.innerHTML;
    saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Saving...';
    saveBtn.disabled = true;

    fetch("/post/" + postId + "/edit/", {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          updatePostContent(postId, data.content, data.visibility);

          var modal = bootstrap.Modal.getInstance(
            document.getElementById("editPostModal")
          );
          modal.hide();
        } else {
          showFormErrors(form, data.errors);
        }
      })
      .catch(function (error) {
        console.error("Save post error:", error);
        alert("Unable to save post: " + error.message);
      })
      .finally(function () {
        saveBtn.innerHTML = originalText;
        saveBtn.disabled = false;
      });
  } catch (error) {
    console.error("JavaScript error:", error);
    alert("An error occurred. Please try again.");
  }
}

function updatePostContent(postId, content, visibility) {
  var postContent = document.querySelector(".card-text");
  if (postContent) {
    postContent.textContent = content;
  }

  var visibilityBadge = document.querySelector(".badge.bg-secondary");
  if (visibilityBadge) {
    visibilityBadge.textContent = visibility;
  }

  var postCards = document.querySelectorAll(`[data-post-id="${postId}"]`);
  postCards.forEach(function (card) {
    var contentEl = card.querySelector(".card-text");
    if (contentEl) {
      contentEl.textContent = content;
    }

    var badgeEl = card.querySelector(".badge");
    if (badgeEl) {
      badgeEl.textContent = visibility;
    }
  });
}

function showFormErrors(form, errors) {
  var existingErrors = form.querySelectorAll(".invalid-feedback");
  existingErrors.forEach(function (error) {
    error.remove();
  });

  Object.keys(errors).forEach(function (fieldName) {
    var field = form.querySelector('[name="' + fieldName + '"]');
    if (field) {
      field.classList.add("is-invalid");
      var errorDiv = document.createElement("div");
      errorDiv.className = "invalid-feedback";
      errorDiv.textContent = errors[fieldName][0];
      field.parentNode.appendChild(errorDiv);
    }
  });
}

let notificationCheckInterval;

function initializeNotificationSystem() {
  if (!document.querySelector('.nav-link[href*="notifications"]')) {
    return;
  }

  notificationCheckInterval = setInterval(checkForNewNotifications, 30000);

  document.addEventListener("visibilitychange", function () {
    if (!document.hidden) {
      checkForNewNotifications();
    }
  });
}

function checkForNewNotifications() {
  fetch("/notifications/count/", {
    method: "GET",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      updateNotificationBadge(data.unread_count);
    })
    .catch((error) => {
      console.log("Notification check error:", error);
    });
}

function updateNotificationBadge(count) {
  let badge = document.getElementById("notification-count");
  let notificationLink = document.querySelector(
    '.nav-link[href*="notifications"]'
  );

  if (count > 0) {
    if (badge) {
      badge.textContent = count;
      badge.style.display = "inline-block";
    } else {
      badge = document.createElement("span");
      badge.id = "notification-count";
      badge.className = "badge bg-danger rounded-pill ms-1 notification-badge";
      badge.textContent = count;
      notificationLink.appendChild(badge);
    }

    if (badge.getAttribute("data-last-count") !== count.toString()) {
      badge.style.animation = "none";
      setTimeout(() => {
        badge.style.animation = "pulse-notification 2s ease-in-out infinite";
      }, 10);
      badge.setAttribute("data-last-count", count.toString());

      if (count > parseInt(badge.getAttribute("data-last-count") || "0")) {
        showNotificationToast("You have new notifications!");
      }
    }
  } else {
    if (badge) {
      badge.style.display = "none";
    }
  }
}

function showNotificationToast(message) {
  const toast = document.createElement("div");
  toast.className =
    "position-fixed top-0 end-0 m-3 alert alert-info alert-dismissible fade show";
  toast.style.zIndex = "1060";
  toast.innerHTML = `
    <i class="fas fa-bell me-2"></i>
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  `;

  document.body.appendChild(toast);

  setTimeout(() => {
    if (toast.parentNode) {
      toast.remove();
    }
  }, 4000);
}

function markNotificationAsRead(notificationId) {
  const csrfToken = getCookie("csrftoken");

  fetch("/notifications/update/", {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
      "X-Requested-With": "XMLHttpRequest",
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `notification_id=${notificationId}`,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        updateNotificationBadge(data.unread_count);
      }
    })
    .catch((error) => {
      console.log("Mark notification read error:", error);
    });
}

function markAllNotificationsAsRead() {
  const csrfToken = getCookie("csrftoken");

  fetch("/notifications/update/", {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
      "X-Requested-With": "XMLHttpRequest",
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: "mark_all=true",
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        updateNotificationBadge(data.unread_count);

        const notificationItems = document.querySelectorAll(
          ".notification-item.unread"
        );
        notificationItems.forEach((item) => {
          item.classList.remove("unread");
        });
      }
    })
    .catch((error) => {
      console.log("Mark all notifications read error:", error);
    });
}

window.markNotificationAsRead = markNotificationAsRead;
window.markAllNotificationsAsRead = markAllNotificationsAsRead;
