document.addEventListener('DOMContentLoaded', function () {
  const multiSelects = document.querySelectorAll('.multi-select');
  multiSelects.forEach(sel => {
    new Choices(sel, {
      removeItemButton: true,
      searchEnabled: true,
      placeholderValue: "選択してください"
    });
  });
});
