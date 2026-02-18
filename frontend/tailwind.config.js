/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: "#2563EB", // Keep for now as accent if needed, or remove later
                secondary: "#1E293B",
                // Custom Palette
                black: "#000000",
                onyx: "#111111",
                carbon: "#232323",
                graphite: "#343434",
                irongrey: "#464646",
                charcoal: "#575757",
                dimgrey: "#696969",
                grey: "#7a7a7a",
            },
            fontFamily: {
                sans: ['Outfit', 'sans-serif'], // Replaced Interform with Outfit
                heading: ['Syne', 'sans-serif'], // Set Syne for headings
            }
        },
    },
    plugins: [],
}
