import './PokemonEntry.css';

function PokemonEntry({name, types, abilities, moves, sprites}) {

    let url = sprites.other["official-artwork"].front_default;

    var stringType = '';

    for(let i = 0; i < types.length; i++) {
        stringType = stringType + types[i].type.name;
        if(i != types.length - 1) {
            stringType = stringType + ', '
        }
    };

    var stringAbility = '';

    for(let i = 0; i < abilities.length; i++) {
        stringAbility = stringAbility + abilities[i].ability.name;
        if(i != abilities.length - 1) {
            stringAbility = stringAbility + ', '
        }
    };

    var stringMove = '';

    for(let i = 0; i < moves.length; i++) {
        if(i >= 10) {
            break;
        }
        stringMove = stringMove + moves[i].move.name;
        if(i != moves.length - 1 && i < 9) {
            stringMove = stringMove + ', '
        }
    };

    return (
        <div className="newPokemonEntry">
            <li>
                <div className="info-container">
                    <div className="image-placeholder">
                        <img src={url} alt='sprite'></img>
                    </div>
                    <div className="info-text">
                        <p>Name: <span className='uppercase'>{name}</span></p>
                        <p>Type: <span className='uppercase'>{stringType}</span></p>
                        <p>Abilities: <span className='uppercase'>{stringAbility}</span></p>
                        <p>Possible Moves: <span className='uppercase'>{stringMove}</span></p>
                    </div>
                </div>
            </li>
        </div>
    );
}

export default PokemonEntry;