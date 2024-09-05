<script lang="ts">
    import { onMount } from 'svelte';

    function handleClick(language: string) {
        if (language === "english") {
            window.location.href = "/en/introduction";
        } else if (language === "czech") {
            window.location.href = "/cz/introduction";
        }
    }

    onMount(async () => {
	    const buttons = document.querySelectorAll("button");
	    buttons.forEach(button => {
		    button.addEventListener("click", () => {
			    const language = button.getAttribute("data-language") as string;
			    handleClick(language);
		    });
	    });
    });



</script>

<style>
    :global(body, html) {
        margin: 0;
	    overflow: hidden;
    }

	.container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
		width: 100vw;
		overflow: hidden;
	}

    .image-button-wrapper {
        display: flex;
	    flex-direction: column;
        justify-content: center;
        align-items: center;
	    overflow: hidden;
    }

    .image-button-wrapper img {
	    max-height: calc(90vh - 55px);
        max-width: 90vw;
        width: auto;
        height: auto;
        box-sizing: border-box;
    }

    .button-row {
        display: flex;
	    padding-top: 10px;
	    width: 100%;
        justify-content: space-between;
	    box-sizing: border-box;
    }

    button {
        padding: 10px 24px;
        font-size: 18px;
	    border-radius: 3px;
        cursor: pointer;
	    background-color: #000;
        color: #fff;
	    border: 2px solid #000;
    }

    button:hover {
	    background-color: #fff;
        color: #000;
    }

    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }

    @keyframes resizeAndMove {
        0% {
            transform: scale(1) translateY(0);
        }
        100% {
            transform: scale(0.75) translateY(-10%);
        }
    }

    @keyframes fadeInButtons {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
</style>

<main>
	main_page
    <div class="container">
        <div class="image-button-wrapper">
	        <img src="/png/logo-light.png" alt="Logo">

	        <div class="button-row">
	            <button data-language="english">Continue (English)</button>
	            <button data-language="czech">Pokračovat (Čeština)</button>
	        </div>
        </div>
    </div>
</main>
