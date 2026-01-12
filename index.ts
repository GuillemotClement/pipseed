#!/usr/bin/env bun
type Commande = {
  short: string;
  long: string;
  description: string;
}

const commands: Commande[] = [
  {
    short: "-h",
    long: "--help",
    description: "Show the manuel",
  },
  {
    short: "-g",
    long: "--generate",
    description: "Start the script for generate new data"
  },
  {
    short: "-q",
    long: "--quit",
    description: "Exit the program",
  }
];

console.log("Welcome to PipSeed, my first fucking CLI tool for generate fake data for seed your beautiful database");
console.log("I hope you will enjoy the bad boy.");
console.log("If you think about new behavior, or find some bug, please, send me email to guillemot.clement@protonmail.com");
console.log("\n");

while(1){
  const inputUser=  prompt("Please, write your instruction :");
  console.log("\n");

  const arrInput = inputUser?.split(" ");
  const cmd = arrInput?.slice(0, 1)[0];
  const args = arrInput?.slice(1);

  if(!cmd){
    console.log("Sorry, you haven't write some commande");
    console.log("You can use '-h' or '--help' for see the manual");
  }

  if(cmd === "-q" || cmd === "--quit"){
    console.log("Goddbye, I hope you enjoyt it !");
    process.exit(0);
  } 

  if(cmd === "-h" || cmd === "--help"){
    commands.forEach((commande) => {
      console.log("Commande courte : ", commande.short);
      console.log("Commande longue: ", commande.long);
      console.log("Description: ", commande.description);
      console.log("----------------------");
    });
}

}

