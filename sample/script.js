document.addEventListener('DOMContentLoaded', function() {
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        const select = dropdown.querySelector('.select');
        const menu = dropdown.querySelector('.dropdown-menu');
        const options = menu.querySelectorAll('li');
        const hiddenInput = dropdown.querySelector('input');

        select.addEventListener('click', function() {
            dropdown.classList.toggle('active');
            if (menu.style.display === 'block') {
                menu.style.display = 'none';
            } else {
                menu.style.display = 'block';
            }
        });

        options.forEach(option => {
            option.addEventListener('click', function() {
                select.querySelector('span').textContent = this.textContent;
                hiddenInput.value = this.id;
                dropdown.classList.remove('active');
                menu.style.display = 'none';
            });
        });

        document.addEventListener('click', function(e) {
            if (!dropdown.contains(e.target)) {
                dropdown.classList.remove('active');
                menu.style.display = 'none';
            }
        });
    });
});
