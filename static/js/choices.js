document.addEventListener('DOMContentLoaded', function () {
    // ページ内のすべての multi-select に Choices.js を適用
    const multiSelects = document.querySelectorAll('.multi-select');

    multiSelects.forEach(sel => {
        new Choices(sel, {
            removeItemButton: true,    // 選択項目を削除可能に
            searchEnabled: true,       // 検索可能
            placeholderValue: "選択してください",
            noResultsText: "該当なし",
            itemSelectText: '',        // 項目選択時のテキスト削除
        });
    });
});
