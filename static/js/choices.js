document.addEventListener('DOMContentLoaded', function () {
  const multiSelects = document.querySelectorAll('.multi-select');
  multiSelects.forEach(sel => {
    new Choices(sel, {
      removeItemButton: true,
      searchEnabled: true,
      placeholderValue: "選択してください"
    });

    // 編集時に選択肢復元
    const selected = sel.getAttribute('data-selected');
    if (selected) {
      selected.split(',').forEach(val => {
        sel.value = val;
      });
    }
  });
});
