import React, { useState } from 'react';
import './SubmissionForm.css';

function SubmissionForm({addPokemon}) {

    const [formText, setFormText] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
    
        if (formText.trim() !== '') {
          addPokemon(formText);
          setFormText('');
        }
    };

    return (
        <div id="search-form">
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Search for a Pokemon to add"
                    id="form"
                    value={formText}
                    onChange={(e) => setFormText(e.target.value)}
                />
                <input type="submit" value="ADD" id="add-button"/>
            </form>
        </div>
    );
}

export default SubmissionForm;