import './App.css';

import React, { useState } from 'react';

import SubmissionForm from './SubmissionForm';
import CreatorButton from './CreatorButton';
import PokemonEntry from './PokemonEntry';
import ClearAllButton from './ClearAllButton';

import banner from './banner-image.jpg';

function App() {

  //pokemonTeam is the array, setPokemon updates the array
  const [pokemonTeam, setPokemon] = useState([]);

  //when debugMode is true, the console will log all pokemon present in the array
  var debugMode = false;

  //prints the number of pokemon added and their names
  function debug() {
    var arrayString =  '';

    for(let i = 0; i < pokemonTeam.length; i++) {

      arrayString = arrayString + pokemonTeam[i].name;

      if(i != pokemonTeam.length - 1) {
          arrayString = arrayString + ', '
      }
    };

    console.log(pokemonTeam.length);
    console.log(arrayString);
  }

  //currently, this add method receives a name and finds the pokemon associated with it via an AJAX call
  //it then adds this pokemon to the pokemonTeam
  function addPokemon(name) {

    //if the number of pokemon being added to this team exceeds 6, it is invalid and we shouldn't add it
    if(pokemonTeam.length >= 6) {
      return;
    }

    //but if we get past that, it means our list is still good to go, and we can try to add the new pokemon
    const xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function () {
      if (this.readyState === 4 && this.status === 200) {
        const newPokemon = JSON.parse(this.responseText);

        //when set is called here, it should add the newPokemon to pokemonTeam
        setPokemon([...pokemonTeam, newPokemon]);
      }
    };

    xhttp.open('GET', 'https://pokeapi.co/api/v2/pokemon/'+name+'/', true); //https://stackoverflow.com/questions/50983150/how-to-pass-a-variable-with-url-on-javascript-fetch-method
    xhttp.send();
  }

  if(debugMode) {
    debug();
  }

  return (
    <div className="body">
      <div className="banner-image">
        <img src={banner} alt="banner-image"/>
      </div>
      <section className="content">
        <header>
          <h1>BUILDING A POKEMON TEAM:</h1>
          <h2>A BASIC GUIDE</h2>
        </header>
        <main>
          <SubmissionForm addPokemon={addPokemon}/>
          <div className="hint-message note">
            <p>PLEASE NOTE: A Pokemon team can only consist of up to 6 Pokemon</p>
          </div>
          <div className="hint-message">
            <p>Hint: Try searching for “blastoise”</p>
          </div>
          <div className="or">
            <h3>OR</h3>
          </div>
          <CreatorButton addPokemon={addPokemon}/>
          {pokemonTeam.length > 0 &&
            <ul id='team-info-list'>
              {pokemonTeam.map((pokemon, index) => ( 
                <PokemonEntry
                  key={index}
                  name={pokemon.name}
                  types={pokemon.types}
                  abilities={pokemon.abilities}
                  moves={pokemon.moves}
                  sprites={pokemon.sprites}
                />
              ))}
            </ul>
          }
          <ClearAllButton array={pokemonTeam} setState={setPokemon}/>
        </main>
      </section>
      <footer>
        <div className="footer-info">
            <div className="copyright footer-subsection">
                <p>Copyright &#169;2023</p>
            </div>
            <div className="image-citations footer-subsection">
                <p>Images:</p>
                <p>https://www.youtube.com/watch?app=desktop&v=yWZTMhjBSmM</p>
            </div>
            <div className="source-citations footer-subsection">
                <p>Sources:</p>
                <p>The Pokemon API: https://pokeapi.co/</p>
            </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
