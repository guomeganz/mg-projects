import './ClearAllButton.css';
import React, { useState } from 'react';

function ClearAllButton({array, setState}) {

    const handleClick = () => {
        setState([]);
    }

    return (
        <div className='clear-all'>
            <button id="clear-all-button" onClick={handleClick}>
                START OVER
            </button>
        </div>
    );
}

export default ClearAllButton;