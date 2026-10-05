// ===== SISTEMA DE CARRINHO DE COMPRAS COM LOCALSTORAGE =====

// Aguarda o DOM carregar
document.addEventListener('DOMContentLoaded', function() {
    
    console.log('🛒 Inicializando carrinho...');
    
    // ===== VARIÁVEIS =====
    let carrinho = [];
    
    // ===== ELEMENTOS =====
    const carrinhoIcone = document.getElementById('carrinho-icone');
    const carrinhoModal = document.getElementById('carrinho-modal');
    const carrinhoFechar = document.getElementById('carrinho-fechar');
    const carrinhoLista = document.getElementById('carrinho-lista');
    const carrinhoTotal = document.getElementById('carrinho-total');
    const carrinhoContador = document.getElementById('carrinho-contador');
    const btnFinalizar = document.getElementById('btn-finalizar');
    
    // ===== FUNÇÕES DE LOCALSTORAGE =====
    
    // Salvar carrinho no localStorage
    function salvarCarrinho() {
        try {
            localStorage.setItem('carrinho', JSON.stringify(carrinho));
            console.log('💾 Carrinho salvo no localStorage');
        } catch (e) {
            console.error('Erro ao salvar carrinho:', e);
        }
    }
    
    // Carregar carrinho do localStorage
    function carregarCarrinho() {
        try {
            const dados = localStorage.getItem('carrinho');
            if (dados) {
                carrinho = JSON.parse(dados);
                console.log('📂 Carrinho carregado do localStorage:', carrinho.length, 'itens');
                return true;
            }
        } catch (e) {
            console.error('Erro ao carregar carrinho:', e);
        }
        return false;
    }
    
    // ===== FUNÇÕES PRINCIPAIS =====
    
    // Adicionar ao carrinho
    window.adicionarAoCarrinho = function(nome, preco, imagem) {
        console.log('📦 Adicionando:', nome);
        
        const itemExistente = carrinho.find(item => item.nome === nome);
        
        if (itemExistente) {
            itemExistente.quantidade += 1;
        } else {
            carrinho.push({
                nome: nome,
                preco: preco,
                imagem: imagem,
                quantidade: 1
            });
        }
        
        atualizarCarrinho();
        animarContador();
        salvarCarrinho(); // SALVA NO LOCALSTORAGE
        
        // Feedback visual
        const mensagem = `${nome} adicionado ao carrinho!`;
        mostrarNotificacao(mensagem);
    };
    
    // Remover do carrinho
    window.removerDoCarrinho = function(nome) {
        console.log('🗑️ Removendo:', nome);
        
        const index = carrinho.findIndex(item => item.nome === nome);
        
        if (index !== -1) {
            if (carrinho[index].quantidade > 1) {
                carrinho[index].quantidade -= 1;
            } else {
                carrinho.splice(index, 1);
            }
        }
        
        atualizarCarrinho();
        salvarCarrinho(); // SALVA NO LOCALSTORAGE
    };
    
    // Notificação temporária
    function mostrarNotificacao(mensagem) {
        // Verifica se já existe uma notificação
        let notificacao = document.querySelector('.notificacao-carrinho');
        
        if (notificacao) {
            notificacao.remove();
        }
        
        notificacao = document.createElement('div');
        notificacao.className = 'notificacao-carrinho';
        notificacao.textContent = mensagem;
        notificacao.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #63b39d;
            color: white;
            padding: 16px 24px;
            border-radius: 12px;
            font-weight: 600;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            z-index: 10000;
            animation: slideUp 0.3s ease;
            max-width: 350px;
        `;
        
        document.body.appendChild(notificacao);
        
        setTimeout(() => {
            notificacao.style.opacity = '0';
            notificacao.style.transition = 'opacity 0.5s';
            setTimeout(() => notificacao.remove(), 500);
        }, 2500);
    }
    
    // Atualizar carrinho
    function atualizarCarrinho() {
        const totalItens = carrinho.reduce((total, item) => total + item.quantidade, 0);
        carrinhoContador.textContent = totalItens;
        
        if (carrinho.length === 0) {
            carrinhoLista.innerHTML = '<p class="carrinho-vazio">🛒 Seu carrinho está vazio</p>';
            carrinhoTotal.textContent = 'R$0,00';
            return;
        }
        
        let html = '';
        let total = 0;
        
        carrinho.forEach(item => {
            const subtotal = item.preco * item.quantidade;
            total += subtotal;
            
            const nomeEscapado = item.nome.replace(/'/g, "\\'");
            
            html += `
                <div class="carrinho-item">
                    <img src="${item.imagem}" alt="${item.nome}" class="carrinho-item-img">
                    <div class="carrinho-item-info">
                        <h4>${item.nome}</h4>
                        <div class="carrinho-item-preco">
                            R$ ${item.preco.toFixed(2)} x ${item.quantidade} = R$ ${subtotal.toFixed(2)}
                        </div>
                    </div>
                    <button class="carrinho-item-remover" onclick="removerDoCarrinho('${nomeEscapado}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `;
        });
        
        carrinhoLista.innerHTML = html;
        carrinhoTotal.textContent = `R$ ${total.toFixed(2)}`;
    }
    
    // Animar contador
    function animarContador() {
        carrinhoContador.classList.remove('pulse');
        void carrinhoContador.offsetWidth;
        carrinhoContador.classList.add('pulse');
    }
    
    // Abrir modal
    function abrirModal() {
        console.log('📂 Abrindo modal...');
        carrinhoModal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
    
    // Fechar modal
    window.fecharModal = function() {
        console.log('📂 Fechando modal...');
        carrinhoModal.classList.remove('active');
        document.body.style.overflow = 'auto';
    };
    
    // Finalizar compra
    function finalizarCompra() {
        if (carrinho.length === 0) {
            alert('🛒 Seu carrinho está vazio!');
            return;
        }
        
        const total = carrinho.reduce((sum, item) => sum + (item.preco * item.quantidade), 0);
        
        let mensagem = 'Olá! Gostaria de finalizar minha compra:%0A%0A';
        
        carrinho.forEach(item => {
            mensagem += `- ${item.nome} (${item.quantidade}x) = R$ ${(item.preco * item.quantidade).toFixed(2)}%0A`;
        });
        
        mensagem += `%0ATotal: R$ ${total.toFixed(2)}`;
        
        const numero = '5511912345678';
        const url = `https://wa.me/${numero}?text=${mensagem}`;
        
        window.open(url, '_blank');
        
        // Limpa carrinho e localStorage
        carrinho = [];
        atualizarCarrinho();
        salvarCarrinho();
        window.fecharModal();
    }
    
    // ===== EVENTOS =====
    
    // Abrir modal ao clicar no ícone
    if (carrinhoIcone) {
        carrinhoIcone.addEventListener('click', function(e) {
            e.stopPropagation();
            console.log('🖱️ Clicou no carrinho');
            abrirModal();
        });
    }
    
    // Fechar modal
    if (carrinhoFechar) {
        carrinhoFechar.addEventListener('click', function(e) {
            e.stopPropagation();
            window.fecharModal();
        });
    }
    
    // Fechar ao clicar fora
    if (carrinhoModal) {
        carrinhoModal.addEventListener('click', function(e) {
            if (e.target === carrinhoModal) {
                window.fecharModal();
            }
        });
    }
    
    // Finalizar compra
    if (btnFinalizar) {
        btnFinalizar.addEventListener('click', finalizarCompra);
    }
    
    // Fechar com ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            window.fecharModal();
        }
    });
    
    // ===== CARREGA CARRINHO SALVO =====
    carregarCarrinho();
    atualizarCarrinho();
    
    console.log('✅ Carrinho inicializado com sucesso!');
    console.log('📦 Itens no carrinho:', carrinho.length);
});