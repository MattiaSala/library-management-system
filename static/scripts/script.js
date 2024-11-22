function openEditModal(bookId, title, author) {
    const modal = document.getElementById('editModal');
    document.getElementById('editBookId').value = bookId;
    document.getElementById('editTitle').value = title;
    document.getElementById('editAuthor').value = author;
    modal.classList.remove('hidden');
  }

  function closeEditModal() {
    document.getElementById('editModal').classList.add('hidden');
  }

  function openAddModal() {
    document.getElementById('addModal').classList.remove('hidden');
  }

  function closeAddModal() {
    document.getElementById('addModal').classList.add('hidden');
  }