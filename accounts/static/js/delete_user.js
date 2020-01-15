function deleteUser(deleteUrl, modalId, rowId, csrfToken) {
    const xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        // Only run if the request is complete
        if (xhr.readyState !== 4) return;

        if (xhr.status === 204) {
            const modal = $('#' + modalId);
            const row = $('#' + rowId);
            modal.modal('hide');
            modal.on('hidden.bs.modal', function () {
                modal.remove();
                row.remove();
            });
        } else if (xhr.status === 404) {
            setModalError(modalId, 'User not found. Perhaps it has been deleted already.')
        } else {
            setModalError(modalId, 'Something went wrong.')
        }
    };

    xhr.open('DELETE', deleteUrl);

    xhr.setRequestHeader('X-CSRFToken', csrfToken);

    xhr.send();
}