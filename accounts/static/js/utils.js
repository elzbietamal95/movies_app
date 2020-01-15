function setModalError(modalId, error) {
    const modalError = $('#' + modalId + ' .modal-error');
    modalError.html(error);
    modalError.removeClass('d-none');
}