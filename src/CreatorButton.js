import './CreatorButton.css';
import React, { useState } from 'react';

function CreatorButton({addPokemon}) {

    return (
        <div className="creator-choice">
            <button id="creator-choice-button" onClick={() => addPokemon("gengar")}>
                CREATOR'S CHOICE
            </button>
        </div>
    );
}

export default CreatorButton;