// Wishlist toggle from book detail
async function toggleWishlist(bookId) {
  try {
    const res = await fetch(`/books/toggle-wishlist/${bookId}`, {
      method: 'POST',
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
    });
    const data = await res.json();
    const btn = document.getElementById('wishbtn');
    if (data.status === 'added') {
      btn.textContent = '♥ In Wishlist';
      btn.classList.remove('btn-outline-danger');
      btn.classList.add('btn-danger');
    } else if (data.status === 'removed') {
      btn.textContent = '♡ Add to Wishlist';
      btn.classList.remove('btn-danger');
      btn.classList.add('btn-outline-danger');
    }
  } catch (e) {
    console.error(e);
    alert('Something went wrong while updating wishlist.');
  }
}

// Remove from wishlist on wishlist page
async function removeFromWishlist(bookId, el) {
  try {
    const res = await fetch(`/books/toggle-wishlist/${bookId}`, {
      method: 'POST',
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
    });
    const data = await res.json();
    if (data.status === 'removed') {
      // remove the card
      const card = el.closest('.col-sm-6, .col-md-4, .col-lg-3');
      if (card) card.remove();
    }
  } catch (e) {
    console.error(e);
  }
}

// My Listings actions (you'll implement these endpoints)
async function toggleActive(bookId, el) {
  try {
    const res = await fetch(`/account/listings/${bookId}/toggle-active`, { method: 'POST' });
    const data = await res.json();
    el.textContent = data.active ? 'Turn Off' : 'Turn On';
  } catch {
    alert('Failed to toggle availability');
  }
}

async function markSold(bookId, el) {
  try {
    const res = await fetch(`/account/listings/${bookId}/mark-sold`, { method: 'POST' });
    if (res.ok) el.innerHTML = '<i class="bi bi-bag-check"></i> Marked Sold';
  } catch { alert('Failed to mark sold'); }
}

async function markGift(bookId, el) {
  try {
    const res = await fetch(`/account/listings/${bookId}/mark-gift`, { method: 'POST' });
    if (res.ok) el.innerHTML = '<i class="bi bi-gift"></i> Marked Gift';
  } catch { alert('Failed to mark gift'); }
}

async function deleteListing(bookId, el) {
  if (!confirm('Delete this listing?')) return;
  try {
    const res = await fetch(`/account/listings/${bookId}/delete`, { method: 'POST' });
    if (res.ok) el.closest('.card').remove();
  } catch { alert('Failed to delete listing'); }
}

function replyToComment(reviewId) {
  // surface a simple prompt -> you can later wire this to a modal
  const text = prompt('Reply to this comment:');
  if (!text) return;
  fetch(`/account/reviews/${reviewId}/reply`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ body: text })
  }).then(r => {
    if (r.ok) alert('Reply posted!');
    else alert('Failed to post reply');
  });
}
