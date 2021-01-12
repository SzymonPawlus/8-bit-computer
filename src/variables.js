export const commands = [
    "BCK",
    "LAI",
    "LAM",
    "STA",
    "LAP",
    "LBI",
    "LBM",
    "OTA",
    "ADD",
    "SUB",
    "CMP",
    "JMP",
    "JMZ",
    "JMC",
    "SAP",
    "HALT",
    "DB"
];

export const coloring = [
    { value: /;.*$/, color: "gray", replace: "$&" },
    { value: "#define", color: "#5e7fff", replace: "#define" },
    { value: /0[xX][0-9a-fA-F]+/, color: "yellow", replace: "$&" },
    { value: /^\.\w+[a-zA-Z0-9_]:/, color: "green", replace: "$&" },
]