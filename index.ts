#!/usr/bin/env bun
type Commande = {
  short: string;
  long: string;
  description: string;
}

type InputUserProps = {
  cmd: string;
  args: string[];
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
  },
];

console.log("Welcome to PipSeed, my first fucking CLI tool for generate fake data for seed your beautiful database");
console.log("I hope you will enjoy the bad boy.");
console.log("If you think about new behavior, or find some bug, please, send me email to guillemot.clement@protonmail.com");
console.log("\n");

while(1){
  const inputUser= prompt("Please, write your instruction :") ?? "";
  console.log("\n");
  const { cmd, args } = extractInput(inputUser);


  switch(cmd){
    case '-q':
    case '--quit':
      console.log("Goddbye, I hope you enjoyt it !");
      process.exit(0);
      break;
    case '-h':
    case '-help':
      commands.forEach((commande) => {
        console.log("Commande courte : ", commande.short);
        console.log("Commande longue: ", commande.long);
        console.log("Description: ", commande.description);
        console.log("----------------------");
      });
      break;

    default: 
      console.log("You can use '-h' or '--help' for see the manual");
  }
}

function extractInput(prompt: string): InputUserProps {
  const arrInput = prompt?.split(" ");
  const cmd = arrInput?.slice(0, 1)[0] ?? "";
  const args = arrInput?.slice(1) ?? [];

  if(!cmd){
    console.log("You haven't write a command");
    return { cmd, args}
  }

  const isShort = cmd.length < 2;
  const isLong = cmd.length > 2;

  if(isShort){
    if(cmd[0] !== '-'){
      console.log("Short command need '-' for the first caracter");
      return { cmd: "", args: []};
    }
  }
  
  if(isLong){
    if(cmd[0] !== '-' && cmd[1] !== '--'){
      console.log("Long command need to start with '--'");
      return { cmd: "", args: []};
    }
  }

  return {
    cmd,
    args
  }
}